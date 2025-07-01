import json
import os

import openai
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from subway_system import SubwaySystem, load_system

load_dotenv()

st.set_page_config(page_title="Subway Route Finder", page_icon="🚇", layout="wide")


@st.cache_resource
def get_upstage_client():
    """Create OpenAI client for Upstage Solar."""
    try:
        client = openai.OpenAI(
            api_key=os.environ.get("UPSTAGE_API_KEY"),
            base_url="https://api.upstage.ai/v1/solar",
        )
        return client
    except TypeError:
        st.error("UPSTAGE_API_KEY 환경 변수가 설정되지 않았습니다. .env 파일을 확인하거나 터미널에서 API 키를 설정해주세요.")
        return None


@st.cache_data
def load_subway() -> SubwaySystem:
    """Load subway graph data with caching."""
    return load_system()


def find_and_display_path(start_station: str, end_station: str, subway: SubwaySystem) -> None:
    """Calculate shortest path and render the result."""
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

    st.success(f"**경로를 찾았습니다! 총 소요 시간: {min_dist}분**")

    summary_parts = [f"**{best_route[0][0]}호선 {best_route[0][1]}** 출발"]
    cumulative_time = 0
    for i in range(len(best_route) - 1):
        cur_node, next_node = best_route[i], best_route[i + 1]
        edge_weight = next((w for n, w in subway.graph[cur_node] if n == next_node), 0)
        cumulative_time += edge_weight
        if cur_node[1] == next_node[1] and cur_node[0] != next_node[0]:
            summary_parts.append(f"**{next_node[0]}호선 {next_node[1]}** 환승 ({cumulative_time}분 소요 예상)")
    summary_parts.append(f"**{best_route[-1][0]}호선 {best_route[-1][1]}** 도착({min_dist}분 소요 예상)")

    st.markdown(f"**경로 요약**: {' → '.join(summary_parts)}")

    with st.expander("자세한 경로 보기"):
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


def main() -> None:
    client = get_upstage_client()
    if not client:
        return

    subway = load_subway()

    with st.sidebar:
        st.title("🚇 Subway Route Finder")
        st.info("출발역과 도착역을 선택하거나, 자연어로 역을 입력해 보세요.")

    st.info("💡 '강남에서 홍대까지'와 같이 입력하면 Solar API가 역을 인식합니다. 또는 직접 역을 선택하세요.")
    st.info("💡 편의상 역 간 이동 시간은 2분, 환승 시간은 5분으로 설정되었습니다.")

    if "last_query" not in st.session_state:
        st.session_state.last_query = ""
    if "start_station" not in st.session_state:
        st.session_state.start_station = ""
    if "end_station" not in st.session_state:
        st.session_state.end_station = ""

    query = st.text_input("자연어로 경로를 질문하세요:", placeholder="예: 강남역에서 시청역 가는 길 알려줘")

    all_stations = sorted(subway.station_nodes.keys())
    auto_search_triggered = False

    if query and query != st.session_state.last_query:
        st.session_state.last_query = query
        with st.spinner("Solar API로 역 이름 분석 중..."):
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that extracts departure and arrival stations from user queries. Respond ONLY with a valid JSON object containing 'departure' and 'arrival' keys."
                    ),
                },
                {"role": "user", "content": "강남역에서 시청역 가는 길 알려줘"},
                {"role": "assistant", "content": "{\"departure\": \"강남\", \"arrival\": \"시청\"}"},
                {"role": "user", "content": "홍대에서 출발해서 잠실까지 가주세요."},
                {"role": "assistant", "content": "{\"departure\": \"홍대입구\", \"arrival\": \"잠실\"}"},
                {"role": "user", "content": "천안에서 서울까지 어떻게 가?"},
                {"role": "assistant", "content": "{\"departure\": \"천안\", \"arrival\": \"서울역\"}"},
                {"role": "user", "content": query},
            ]
            try:
                response = client.chat.completions.create(model="solar-pro2-preview", messages=messages, temperature=0.1)
                result = json.loads(response.choices[0].message.content)
                raw_start = result.get("departure")
                raw_end = result.get("arrival")
                start_station_nlp = raw_start if raw_start in all_stations else (raw_start + "역" if raw_start and raw_start + "역" in all_stations else None)
                end_station_nlp = raw_end if raw_end in all_stations else (raw_end + "역" if raw_end and raw_end + "역" in all_stations else None)
                if start_station_nlp and end_station_nlp:
                    st.session_state.start_station = start_station_nlp
                    st.session_state.end_station = end_station_nlp
                    auto_search_triggered = True
                else:
                    st.warning("API가 역 이름을 정확히 인식하지 못했습니다. 아래에서 직접 선택해주세요.")
                    st.session_state.start_station = ""
                    st.session_state.end_station = ""
            except Exception as e:
                st.error(f"API 호출 중 오류가 발생했습니다: {e}")

    col1, col2 = st.columns(2)
    start_index = all_stations.index(st.session_state.start_station) if st.session_state.start_station in all_stations else 0
    end_index = all_stations.index(st.session_state.end_station) if st.session_state.end_station in all_stations else 0

    with col1:
        start_station = st.selectbox("🚩 출발역", all_stations, index=start_index, placeholder="출발역 선택")
    with col2:
        end_station = st.selectbox("🏁 도착역", all_stations, index=end_index, placeholder="도착역 선택")

    if st.button("경로 찾기", use_container_width=True, type="primary"):
        find_and_display_path(start_station, end_station, subway)
    elif auto_search_triggered:
        find_and_display_path(st.session_state.start_station, st.session_state.end_station, subway)


if __name__ == "__main__":
    main()
