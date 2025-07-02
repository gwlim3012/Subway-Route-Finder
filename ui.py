import pandas as pd
import streamlit as st

from subway_system import SubwaySystem


def render_sidebar() -> None:
    """Renders the sidebar content."""
    with st.sidebar:
        st.title("🚇 Subway Route Finder")
        st.info("출발역과 도착역을 선택하거나, 자연어로 경로를 질문해 보세요.")


def render_main_info() -> None:
    """Renders the main information block."""
    st.info("💡 '강남에서 홍대까지'와 같이 입력하면 Solar API가 역을 인식합니다. 또는 직접 역을 선택하세요.")
    st.info("💡 편의상 역 간 이동 시간은 2분, 환승 시간은 5분으로 설정되었습니다.")


def render_user_inputs(all_stations: list[str]) -> tuple[str, str, str]:
    """Renders user input elements and returns the query, start, and end stations."""
    query = st.text_input("자연어로 경로를 질문하세요:", placeholder="예: 강남역에서 시청역 가는 길 알려줘")

    col1, col2 = st.columns(2)
    start_index = all_stations.index(st.session_state.start_station) if st.session_state.start_station in all_stations else 0
    end_index = all_stations.index(st.session_state.end_station) if st.session_state.end_station in all_stations else 0

    with col1:
        start_station = st.selectbox("🚩 출발역", all_stations, index=start_index, placeholder="출발역 선택")
    with col2:
        end_station = st.selectbox("🏁 도착역", all_stations, index=end_index, placeholder="도착역 선택")

    return query, start_station, end_station


def display_path_result(start_station: str, end_station: str, subway: SubwaySystem, client) -> None:
    """Calculates the shortest path and renders the result, including AI-generated content."""
    from ai_helper import get_route_commentary, get_location_recommendation  # Lazy import

    if not start_station or not end_station:
        st.error("출발역과 도착역을 모두 지정해야 합니다.")
        return
    if start_station == end_station:
        st.warning("출발역과 도착역이 동일합니다.")
        return

    start_nodes = subway.station_nodes.get(start_station, [])
    end_nodes = subway.station_nodes.get(end_station, [])

    best_route = None
    min_dist = float("inf")

    with st.spinner("최단 경로를 계산하는 중입니다..."):
        for s_node in start_nodes:
            for e_node in end_nodes:
                route, dist = subway.shortest_path(s_node, e_node)
                if route and dist < min_dist:
                    min_dist = dist
                    best_route = route

    st.write("---")

    if best_route is None:
        st.error("경로를 찾을 수 없습니다.")
        return

    # --- 경로 요약 및 AI 코멘트 ---
    with st.container(border=True):
        summary_parts = [f"**{best_route[0][0]}호선 {best_route[0][1]}** 출발"]
        cumulative_time = 0
        for i in range(len(best_route) - 1):
            cur_node, next_node = best_route[i], best_route[i + 1]
            edge_weight = next((w for n, w in subway.graph[cur_node] if n == next_node), 0)
            cumulative_time += edge_weight
            if cur_node[1] == next_node[1] and cur_node[0] != next_node[0]:
                summary_parts.append(f"**{next_node[0]}호선 {next_node[1]}** 환승 ({cumulative_time}분 소요 예상)")
        summary_parts.append(f"**{best_route[-1][0]}호선 {best_route[-1][1]}** 도착({min_dist}분 소요 예상)")
        route_summary_text = ' → '.join(summary_parts)

        ai_comment = get_route_commentary(client, route_summary_text)
        st.success(f"**경로 총 소요 시간: {min_dist}분** | {ai_comment}")
        st.markdown(f"**경로 요약**: {route_summary_text}")

    # --- 상세 경로 --- 
    with st.expander("자세한 경로 보기"):
        with st.container(border=True):
            rows = []
            acc_time = 0
            for i in range(len(best_route) - 1):
                cur_node, next_node = best_route[i], best_route[i + 1]
                edge_weight = next((w for n, w in subway.graph[cur_node] if n == next_node), 0)
                acc_time += edge_weight
                cur_line, cur_stn = cur_node
                next_line, next_stn = next_node
                move_type = "환승" if cur_stn == next_stn and cur_line != next_line else "이동"
                rows.append(
                    {
                        "구간": f"{cur_stn} ({cur_line} → {next_line}호선)" if move_type == "환승" else f"{cur_stn} → {next_stn}",
                        "소요 시간": f"+{edge_weight}분",
                        "총 시간": f"{acc_time}분",
                        "구분": move_type,
                    }
                )
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)

    # --- AI 기반 주변 정보 추천 --- 
    st.write("")
    with st.container(border=True):
        st.subheader("🤖 AI가 알려주는 주변 정보")
        rec_col1, rec_col2 = st.columns(2)

        def render_recommendation_section(station_name: str, side: str):
            with st.container():
                st.markdown(f"##### **{station_name}** 주변")
                interest_key = f"{side}_interest_{station_name}"
                if interest_key not in st.session_state:
                    st.session_state[interest_key] = ""

                def set_interest(value):
                    st.session_state[interest_key] = value

                button_col1, button_col2, button_col3 = st.columns(3)
                with button_col1:
                    st.button("맛집 🍽️", on_click=set_interest, args=["맛집"], key=f"{side}_food_{station_name}", use_container_width=True)
                with button_col2:
                    st.button("카페 ☕", on_click=set_interest, args=["카페"], key=f"{side}_cafe_{station_name}", use_container_width=True)
                with button_col3:
                    st.button("볼거리 ✨", on_click=set_interest, args=["볼거리"], key=f"{side}_sights_{station_name}", use_container_width=True)

                interest = st.text_input(
                    f"무엇을 찾으시나요?",
                    placeholder="예: 맛집, 카페, 볼거리",
                    key=interest_key,
                )

                if st.button(f"{station_name} 주변 정보 검색", key=f"{side}_rec_{station_name}"):
                    if interest:
                        recommendation = get_location_recommendation(client, station_name, interest)
                        st.session_state.recommendations[side] = recommendation
                    else:
                        st.warning("궁금한 점을 입력해주세요.")
                
                if side in st.session_state.recommendations:
                    with st.container(border=True):
                        st.markdown(st.session_state.recommendations[side])

        with rec_col1:
            render_recommendation_section(start_station, "start")

        with rec_col2:
            render_recommendation_section(end_station, "end")
