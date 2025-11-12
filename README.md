# Subway Route Finder

Streamlit을 활용하여 제작된 수도권 지하철 최단 경로 안내 및 주변 정보 추천 서비스입니다.

이 프로젝트는 대학교 **자료구조 및 알고리즘(DA)** 수업의 팀 과제로 시작되어 Streamlit으로 웹 UI를 구현하고, Upstage Solar API를 연동하여 자연어 처리 기능을 추가한 토이 프로젝트로 발전시켰습니다.

## 주요 기능

- **자연어 경로 검색**: "강남에서 홍대까지"와 같은 일상적인 언어로 경로를 질문할 수 있습니다.
- **AI 경로 코멘트**: 검색된 경로의 특징(환승 여부, 소요 시간 등)을 AI가 분석하여 코멘트를 제공합니다.
- **AI 주변 정보 추천**: 출발역과 도착역 주변의 맛집, 카페, 볼거리 등을 AI에게 질문하고 추천받을 수 있습니다.
- **최단 경로 계산**: 다익스트라 알고리즘을 기반으로 가장 빠른 경로를 계산합니다.
- **사용자 친화적 UI**: Streamlit을 사용하여 모든 정보를 시각적으로 명확하고 직관적으로 제공합니다.

> **참고**: 이 프로젝트는 학습 및 데모 목적으로 제작되었기 때문에, 역 간 이동 시간과 환승 시간은 단순화를 위해 고정된 값을 사용합니다.
  따라서 실제 지하철 운행 시간 및 경로와는 차이가 있습니다.

## 파일 구조

```
├───.env # Upstage API (private)
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

## 설치 및 실행

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

## 데모 화면

- **메인 화면 및 자연어 검색**
  ![image](https://github.com/user-attachments/assets/988be40c-2212-4297-8988-eba1a609b76e)

- **경로 검색 결과 및 AI 코멘트**
  ![image](https://github.com/user-attachments/assets/a2b7ea2a-a28f-4f93-8aad-7536f5d55471)
  ![image](https://github.com/user-attachments/assets/13dee666-3eae-4a30-8de7-be4f4b940357)


- **AI 주변 정보 추천**
  ![image](https://github.com/user-attachments/assets/1e02d3e7-6a67-4eea-ae52-650a62987944)
