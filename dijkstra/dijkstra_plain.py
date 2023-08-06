def get_next(nodes_to_visit):
    node, _ = min(nodes_to_visit.items(), key=lambda x: x[1][0])
    return node

def dijkstra(graph, source, dest):
    nodes_to_visit = {node: (float('inf'), None) for node in graph}
    nodes_to_visit[source] = (0, None)

    nodes_visited = {}

    while nodes_to_visit:
        next_node = get_next(nodes_to_visit)
        nodes_visited[next_node] = nodes_to_visit[next_node]
        if next_node == dest:
            shortest_distance = nodes_to_visit[next_node][0]
            path = [dest]
            while nodes_visited[next_node][1] is not None:
                next_node = nodes_visited[next_node][1]
                path.append(next_node)
            path.reverse()
            return shortest_distance, path
        current_distance = nodes_to_visit[next_node][0]
        nodes_to_visit.pop(next_node)
        for neighbor, dist in graph[next_node].items():
            if neighbor not in nodes_to_visit:
                continue
            distance = current_distance + dist
            if distance < nodes_to_visit[neighbor][0]:
                nodes_to_visit[neighbor] = (distance, next_node)


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
    dest_node = 'E'
    shortest_distance, path = dijkstra(graph, source_node, dest_node)

    print("Shortest distances from node {} to {}: {}".format(source_node, dest_node, shortest_distance))
    print("Shortest path: {}".format(path))
