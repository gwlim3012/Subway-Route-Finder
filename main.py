import streamlit as st
from dotenv import load_dotenv

from ai_helper import extract_stations_from_query, get_upstage_client
from subway_system import SubwaySystem
from ui import display_path_result, render_main_info, render_sidebar, render_user_inputs

load_dotenv()

st.set_page_config(page_title="Subway Route Finder", page_icon="🚇", layout="wide")


@st.cache_data
def load_subway() -> SubwaySystem:
    """Load subway graph data with caching."""
    return SubwaySystem.from_data_files()


def initialize_session_state() -> None:
    """Initializes session state variables."""
    if "last_query" not in st.session_state:
        st.session_state.last_query = ""
    if "start_station" not in st.session_state:
        st.session_state.start_station = ""
    if "end_station" not in st.session_state:
        st.session_state.end_station = ""
    if "search_result" not in st.session_state:
        st.session_state.search_result = None
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = {}


def handle_new_search(start_station: str, end_station: str, subway: SubwaySystem, client) -> None:
    """Handles a new route search, clearing old recommendations."""
    st.session_state.recommendations = {}  # Reset recommendations
    st.session_state.search_result = {
        "start": start_station,
        "end": end_station,
    }


def main() -> None:
    """Main function to run the Streamlit app."""
    client = get_upstage_client()
    if not client:
        return

    subway = load_subway()
    all_stations = sorted(subway.station_nodes.keys())

    initialize_session_state()
    render_sidebar()
    render_main_info()

    query, start_station, end_station = render_user_inputs(all_stations)

    auto_search_triggered = False
    if query and query != st.session_state.last_query:
        st.session_state.last_query = query
        start_nlp, end_nlp = extract_stations_from_query(client, query, all_stations)
        if start_nlp and end_nlp:
            st.session_state.start_station = start_nlp
            st.session_state.end_station = end_nlp
            handle_new_search(start_nlp, end_nlp, subway, client)
            auto_search_triggered = True
            st.rerun()
        else:
            st.warning("API가 역 이름을 정확히 인식하지 못했습니다. 아래에서 직접 선택해주세요.")
            st.session_state.start_station = ""
            st.session_state.end_station = ""
            st.session_state.search_result = None

    st.session_state.start_station = start_station
    st.session_state.end_station = end_station

    if st.button("경로 찾기", use_container_width=True, type="primary"):
        handle_new_search(start_station, end_station, subway, client)

    if st.session_state.search_result:
        display_path_result(
            st.session_state.search_result["start"],
            st.session_state.search_result["end"],
            subway,
            client,
        )


if __name__ == "__main__":
    main()
