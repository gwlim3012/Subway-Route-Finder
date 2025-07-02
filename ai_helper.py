import json
import os

import openai
import streamlit as st


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


def extract_stations_from_query(client: openai.OpenAI, query: str, all_stations: list[str]) -> tuple[str | None, str | None]:
    """Extracts departure and arrival stations from a user query using Solar API."""
    with st.spinner("Solar API로 역 이름 분석 중..."):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that extracts departure and arrival stations from user queries. "
                    "Respond ONLY with a valid JSON object containing 'departure' and 'arrival' keys."
                ),
            },
            {"role": "user", "content": "강남역에서 시청역 가는 길 알려줘"},
            {"role": "assistant", "content": '{"departure": "강남", "arrival": "시청"}'},
            {"role": "user", "content": "홍대에서 출발해서 잠실까지 가주세요."},
            {"role": "assistant", "content": '{"departure": "홍대입구", "arrival": "잠실"}'},
            {"role": "user", "content": "천안에서 서울까지 어떻게 가?"},
            {"role": "assistant", "content": '{"departure": "천안", "arrival": "서울역"}'},
            {"role": "user", "content": query},
        ]
        try:
            response = client.chat.completions.create(model="solar-pro2-preview", messages=messages, temperature=0.1)
            result = json.loads(response.choices[0].message.content)
            raw_start = result.get("departure")
            raw_end = result.get("arrival")

            def find_station(name: str) -> str | None:
                if not name:
                    return None
                if name in all_stations:
                    return name
                if f"{name}역" in all_stations:
                    return f"{name}역"
                return None

            start_station = find_station(raw_start)
            end_station = find_station(raw_end)

            return start_station, end_station
        except Exception as e:
            st.error(f"API 호출 중 오류가 발생했습니다: {e}")
            return None, None


def get_route_commentary(client: openai.OpenAI, route_summary: str) -> str:
    """Generates a brief, friendly comment about the calculated route."""
    with st.spinner("AI가 경로에 대한 코멘트를 생성 중입니다..."):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful subway route assistant. "
                    "Given a route summary, provide a short, friendly, and helpful one-sentence comment in Korean. "
                    "Focus on aspects like transfers, total time, or general convenience."
                ),
            },
            {"role": "user", "content": "경로 요약: **2호선 강남** 출발 → **2호선 삼성** 도착(4분 소요 예상)"},
            {"role": "assistant", "content": "환승 없이 빠르게 이동할 수 있는 좋은 경로네요!"},
            {"role": "user", "content": "경로 요약: **1호선 시청** 출발 → **2호선 시청** 환승 (5분 소요 예상) → **2호선 홍대입구** 도착(15분 소요 예상)"},
            {"role": "assistant", "content": "환승이 한 번 있지만, 총 소요 시간이 짧아 편리한 경로입니다."},
            {"role": "user", "content": route_summary},
        ]
        try:
            response = client.chat.completions.create(model="solar-pro2-preview", messages=messages, temperature=0.7)
            return response.choices[0].message.content
        except Exception:
            return "경로를 찾았습니다!"


def get_location_recommendation(client: openai.OpenAI, station: str, interest: str) -> str:
    """Gets recommendations for a given station and interest."""
    with st.spinner(f"{station}역 주변 {interest} 정보를 AI로 검색 중..."):
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that provides recommendations for places around a given subway station in Korea. Respond in Korean.",
            },
            {"role": "user", "content": f"{station}역 주변 {interest} 추천해줘."},
        ]
        try:
            response = client.chat.completions.create(model="solar-pro2-preview", messages=messages, temperature=0.7)
            return response.choices[0].message.content
        except Exception as e:
            return f"API 호출 중 오류가 발생했습니다: {e}"
