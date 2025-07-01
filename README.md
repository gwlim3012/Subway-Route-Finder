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
  ![image](https://github.com/user-attachments/assets/3b9c51f4-1641-4aaa-b4ea-f126c6abe214)


- Manual selection: You can also specify departure and arrival stations directly.
  ![image](https://github.com/user-attachments/assets/02900252-e85d-427c-95f3-b7b61c48f095)


- Detailed output: The shortest path, route summary, and total estimated travel time are displayed.
  ![image](https://github.com/user-attachments/assets/87172686-8149-4f1e-9042-f292e117552f)


