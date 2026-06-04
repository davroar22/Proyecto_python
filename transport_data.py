from collections import defaultdict
import heapq
import pandas as pd


class TransportGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.stations = set()

    def add_connection(self, origin, destination, time_cost, route_name):
        self.graph[origin].append((destination, time_cost, route_name))
        self.graph[destination].append((origin, time_cost, route_name))
        self.stations.add(origin)
        self.stations.add(destination)

    def shortest_path(self, start, end, transfer_penalty=4):
        pq = [(0, start, [], None, 0, [])]
        visited = {}

        while pq:
            total_cost, current, path, current_route, transfers, route_history = heapq.heappop(pq)

            state_key = (current, current_route)
            if state_key in visited and visited[state_key] <= total_cost:
                continue
            visited[state_key] = total_cost

            new_path = path + [current]

            if current == end:
                return {
                    "total_cost": total_cost,
                    "path": new_path,
                    "transfers": transfers,
                    "routes_used": route_history,
                }

            for neighbor, edge_cost, route_name in self.graph[current]:
                extra_penalty = 0
                new_transfers = transfers
                new_route_history = route_history.copy()

                if current_route is None:
                    if not new_route_history or new_route_history[-1] != route_name:
                        new_route_history.append(route_name)
                elif route_name != current_route:
                    extra_penalty = transfer_penalty
                    new_transfers += 1
                    if not new_route_history or new_route_history[-1] != route_name:
                        new_route_history.append(route_name)
                elif not new_route_history:
                    new_route_history.append(route_name)

                new_cost = total_cost + edge_cost + extra_penalty

                heapq.heappush(
                    pq,
                    (
                        new_cost,
                        neighbor,
                        new_path,
                        route_name,
                        new_transfers,
                        new_route_history,
                    ),
                )

        return None


def build_network_from_csv(csv_path="network_edges.csv"):
    df = pd.read_csv(csv_path)
    graph = TransportGraph()

    for _, row in df.iterrows():
        graph.add_connection(
            row["origin"],
            row["destination"],
            int(row["time_cost"]),
            row["route_name"],
        )

    return graph