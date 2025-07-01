import json
import heapq
from pathlib import Path


class SubwaySystem:
    """Graph-based subway network with quick station lookup."""

    def __init__(self):
        self.graph = {}
        self.station_nodes = {}

    def add_station(self, line: str, station: str) -> None:
        node = (line, station)
        self.graph.setdefault(node, [])
        self.station_nodes.setdefault(station, []).append(node)

    def add_connection(
        self,
        line_a: str,
        station_a: str,
        line_b: str,
        station_b: str,
        weight: int,
    ) -> None:
        self.graph[(line_a, station_a)].append(((line_b, station_b), weight))
        self.graph[(line_b, station_b)].append(((line_a, station_a), weight))

    def dijkstra(self, start, end):
        distances = {node: float("inf") for node in self.graph}
        distances[start] = 0
        previous = {node: None for node in self.graph}
        queue = [(0, start)]
        visited = set()

        while queue:
            current_dist, current = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)
            if current == end:
                break

            for neighbor, weight in self.graph[current]:
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(queue, (new_dist, neighbor))

        return distances[end], previous

    def shortest_path(self, start, end):
        dist, prev = self.dijkstra(start, end)
        if dist == float("inf"):
            return None, float("inf")
        path = []
        node = end
        while node:
            path.append(node)
            node = prev[node]
        return list(reversed(path)), dist


def load_system() -> SubwaySystem:
    """Load graph data from the data folder."""
    system = SubwaySystem()
    data_path = Path(__file__).parent / "data"
    stations_file = data_path / "stations.json"
    transfers_file = data_path / "transfers.json"
    with open(stations_file, encoding="utf-8") as f:
        stations = json.load(f)
    with open(transfers_file, encoding="utf-8") as f:
        transfers = json.load(f)
    for line_str, st_list in stations.items():
        for i, stn in enumerate(st_list):
            system.add_station(line_str, stn)
            if i > 0:
                prev = st_list[i - 1]
                system.add_connection(line_str, prev, line_str, stn, 2)
    for l1, s1, l2, s2 in transfers:
        system.add_connection(str(l1), s1, str(l2), s2, 5)
    return system
