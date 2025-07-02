# 🚇 AI Subway Route Finder

AI와 Streamlit을 활용하여 제작된 수도권 지하철 최단 경로 안내 및 주변 정보 추천 서비스입니다.

이 프로젝트는 대학교 2학년 1학기 **자료구조 및 알고리즘(DA)** 수업의 팀 과제로 시작되었습니다. 초기 버전은 **다익스트라 알고리즘**을 사용하여 최단 경로를 콘솔에 출력하는 간단한 프로그램이었습니다. 이후 Streamlit으로 웹 UI를 구현하고, Upstage Solar API를 연동하여 자연어 처리 기능을 추가한 토이 프로젝트로 발전했습니다.

## ✨ 주요 기능

- **자연어 경로 검색**: "강남에서 홍대까지"와 같은 일상적인 언어로 경로를 질문할 수 있습니다.
- **AI 경로 코멘트**: 검색된 경로의 특징(환승 여부, 소요 시간 등)을 AI가 분석하여 친절한 코멘트를 제공합니다.
- **AI 주변 정보 추천**: 출발역과 도착역 주변의 맛집, 카페, 볼거리 등을 AI에게 질문하고 추천받을 수 있습니다.
- **최단 경로 계산**: 다익스트라 알고리즘을 기반으로 가장 빠른 경로를 계산합니다.
- **사용자 친화적 UI**: Streamlit을 사용하여 모든 정보를 시각적으로 명확하고 직관적으로 제공합니다.

> **참고**: 편의상 역 간 이동 시간은 **2분**, 환승 시간은 **5분**으로 고정되어 있습니다.

## 🛠️ 파일 구조

```
C:/Users/world/OneDrive/Desktop/test/
├───.env
├───README.md
├───requirements.txt
├───main.py             # 애플리케이션 메인 로직
├───ui.py               # Streamlit UI 컴포넌트
├───ai_helper.py        # Upstage Solar API 연동 헬퍼
├───subway_system.py    # 지하철 노선도 그래프 및 경로 탐색
├───data/
│   ├───stations.json   # 역 정보
│   └───transfers.json  # 환승 정보
└───__pycache__/ 
```

## ⚙️ 설치 및 실행

1.  **필요한 라이브러리 설치:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **API 키 설정:**
    프로젝트 루트 디렉토리에 `.env` 파일을 생성하고, 아래와 같이 Upstage API 키를 입력합니다.

    ```
    UPSTAGE_API_KEY="YOUR_API_KEY_HERE"
    ```

3.  **애플리케이션 실행:**

    ```bash
    streamlit run main.py
    ```

## 🖼️ 데모 화면

- **메인 화면 및 자연어 검색**
  <img width="700" alt="main" src="https://github.com/user-attachments/assets/f373533f-092c-4377-ab5b-e3fa063a1be5">

- **경로 검색 결과 및 AI 코멘트**
  <img width="700" alt="result" src="https://github.com/user-attachments/assets/1379a2d0-8ed7-4d58-9494-d15a2cfc1323">

- **AI 주변 정보 추천**
  <img width_="700" alt="recommendation" src="https://github.com/ryu-seung-min/subway-route-finder/assets/112821134/b09a781a-e503-4b1b-a20c-0e88389a3339">