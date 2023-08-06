import heapq

def dijkstra(graph, source):
    # Initialize distances and visited nodes
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    visited = set()
    heap = [(0, source)]  # (distance, node)

    while heap:
        current_distance, current_node = heapq.heappop(heap)

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (distance, neighbor))

    return distances

# Example usage:
if __name__ == "__main__":
    # Sample weighted graph represented as an adjacency dictionary
    graph = {
        'A': {'C': 3, 'F': 2},
        'C': {'A': 3, 'F': 2, 'D': 4, 'E':1},
        'F': {'A': 2, 'C': 2, 'E': 3, 'B': 6},
        'E': {'C': 1, 'F': 3, 'B': 2},
        'D': {'B': 1, 'C': 4},
        'B': {'D': 1, 'E': 2, 'F': 6}
    }

    source_node = 'A'
    shortest_distances = dijkstra(graph, source_node)

    print("Shortest distances from source node {}: {}".format(source_node, shortest_distances))
