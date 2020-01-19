"""
Problem set 2 of coursera algo2 pset.
Calculate distance from node 1 to the following nodes
7,37,59,82,99,115,133,165,188,197
return csv of distances
"""


class Dijkstra:

    def __init__(self, weighted_adj_list):
        self.weighted_adj_list = weighted_adj_list

    def shortestPaths(self, source):
        "Calculate shortest paths to all nodes given source node"
        shortest_distances = {source: 0}
        for node in self.weighted_adj_list.keys():
            if node != source:
                shortest_distances[node] = None
        crossing_paths = self.weighted_adj_list[source]
        while(crossing_paths):
            # first finding closest node
            min_path = None
            closest_node = None
            for node, dist in crossing_paths.items():
                if min_path is None or dist < min_path:
                    min_path = dist
                    closest_node = node
            # adding closest node to explored and shortest distances
            # removing node from crossing paths
            # updating crossing paths and distances
            shortest_distances[closest_node] = min_path
            del crossing_paths[closest_node]
            for node, dist in self.weighted_adj_list[closest_node].items():
                if shortest_distances[node] is None:
                    new_dist = dist + min_path
                    curr_dist = crossing_paths.get(node, new_dist)
                    crossing_paths[node] = min(curr_dist, new_dist)

        return shortest_distances


test_graph = {
    1: {2: 3, 3: 2, },
    2: {1: 3, 3: 2, 4: 3, },
    3: {1: 2, 4: 1, },
    4: {2: 3, 3: 1, }
}


def main():
    weighted_adj_list = {}
    with open(
        "/Users/brendonsullivan/Documents/docs/coursera_hw/djkstra.txt",
        'r'
    ) as f:
        for line in f:
            row = line.split('\t')
            head = int(row[0])
            weighted_adj_list[head] = {}
            for i in range(1, len(row)-1):
                node, distance = row[i].split(',')
                weighted_adj_list[head][int(node)] = int(distance)
    paths = Dijkstra(weighted_adj_list).shortestPaths(1)
    nodes = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    filter_dist = [str(paths[i]) for i in nodes]
    print(','.join(filter_dist))


if __name__ == "__main__":
    main()
