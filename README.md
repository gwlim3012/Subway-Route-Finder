# Subway Route Finder

A Streamlit-based web application that finds the shortest path between subway stations in the Seoul metropolitan area.

This project originated as a team assignment for the **Data Structures and Algorithms (DA)** course in the 2nd year, 1st semester of university. The original version was a console-based program that simply displayed the shortest subway route using **Dijkstra's algorithm**. It has since been extended into a more interactive toy project with a web UI built using Streamlit and natural language input supported via an LLM (Large Language Model).

The integrated LLM is **Upstage's Solar-Pro2-preview**, which enables the system to interpret queries such as “강남역에서 서울역까지 알려줘” in Korean and return the optimal route.

For simplicity, the following heuristic assumptions are applied:
- Travel time between adjacent stations: **2 minutes**
- Transfer time between lines: **5 minutes**

## Features

- Natural language queries for subway routing (Korean)
- Dijkstra-based shortest path calculation
- Intuitive Streamlit web UI
- Visual route summary with time estimates

## Requirements

- Python 3.10+
- streamlit
- pandas
- openai
- python-dotenv

## Setup

1. Install dependencies:
 
```bash
pip install -r requirements.txt
```

2. Set your `UPSTAGE_API_KEY` in a `.env` file or your environment.

3. Run the application:

```bash
streamlit run SRF.py
```

## Demo

- Natural language input: Enter queries like “강남역에서 서울역까지 알려줘” and get the shortest route automatically.
  ![image](https://github.com/user-attachments/assets/f373533f-092c-4377-ab5b-e3fa063a1be5)

- Manual selection: You can also specify departure and arrival stations directly.
  ![image](https://github.com/user-attachments/assets/62a38dd6-1207-41dc-ad46-e4559934ace8)

- Detailed output: The shortest path, route summary, and total estimated travel time are displayed.
  ![image](https://github.com/user-attachments/assets/1379a2d0-8ed7-4d58-9494-d15a2cfc1323)
