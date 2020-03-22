"""
The first line indicates the number of vertices and edges, respectively.
Each subsequent line describes an edge (the first two numbers are its tail and head,
respectively) and its length (the third number).
NOTE: some of the edge lengths are negative.
NOTE: These graphs may or may not have negative-cost cycles.

Your task is to compute the "shortest shortest path".
Precisely, you must first identify which, if any, of the three graphs have no negative cycles.
For each such graph, you should compute all-pairs shortest paths and remember the smallest one (i.e., compute minu,v∈Vd(u,v), where d(u,v)d(u,v)
denotes the shortest-path distance from uu to vv).

If each of the three graphs has a negative-cost cycle, then enter "NULL" in the box below.
If exactly one graph has no negative-cost cycles, then enter the length of its shortest shortest path in the box below.
If two or more of the graphs have no negative-cost cycles, then enter the smallest of the lengths of their shortest shortest paths in the box below.
""" # noqa
import numpy as np
import heapq


class Graph:
    """
    Stores graph as {tail_node: {head_node: edge_weight}}
    Initialize with list of weighted edge tuples or add incrementally
    Has reverse lookup for convenience getting in_deg nodes
    """
    def __init__(self, weighted_edges=[]):
        """
        Build graph from list of weighted edges
        weighted edges can be none (builds empty graph),
        but non-null edges must be of format (tail, head, weight)
        """
        self.graph = {}
        self.rev_graph = {}
        self.size = len(self.graph)  # size represents # nodes not edges
        for edge in weighted_edges:
            tail, head, weight = edge
            self.add_edge(tail, head, weight)

    def __len__(self):
        return self.size

    def add_edge(self, tail, head, weight):
        if self.graph.get(tail):
            self.graph.get(tail).update({head: weight})
        else:
            self.graph[tail] = {head: weight}
            self.size += 1  # we added the tail to the graph

        if self.rev_graph.get(head):
            self.rev_graph.get(head).update({tail: weight})
        else:
            self.rev_graph[head] = {tail: weight}

        # add head to graph with no edges if not present
        if not self.graph.get(head):
            self.graph[head] = {}
            self.size += 1  # we added the head to the graph

    def del_edge(self, tail, head):
        self.graph[tail].pop(head)
        self.rev_graph[head].pop(tail)

    def add_node(self, node, to_nodes={}, from_nodes={}):
        # adding inbound edges
        for in_node, weight in from_nodes.items():
            self.add_edge(in_node, node, weight)
        # adding outbound edges
        for out_node, weight in to_nodes.items():
            self.add_edge(node, out_node, weight)

    def del_node(self, node):
        # cleaning up nodes with edges from source
        out_edges = self.graph.pop(node, {})
        for out_node in out_edges.keys():
            self.rev_graph[out_node].pop(node)
        # cleaning up nodes with edges to source
        in_edges = self.rev_graph.pop(node, {})
        for in_node in in_edges.keys():
            self.graph[in_node].pop(node)
        self.size -= 1

    def update_edge_weight(self, tail, head, weight):
        assert isinstance(weight, (int, float)),\
            f'Non-integer weight: {type(weight)}'
        self.graph[tail][head] = weight

    def all_nodes(self):
        return self.graph.keys()

    def get_out_edges(self, node):
        return self.graph.get(node, {}).items()

    def get_in_edges(self, node):
        return self.rev_graph.get(node, {}).items()


def bellman_ford(graph, source, debug=False):
    """
    Calculate shortest paths to all nodes from source
    Returns dictionary of {key, shortest_path_len}
    """
    # initialize
    curr_distances = {}
    for node in graph.all_nodes():
        if node != source:
            curr_distances[node] = np.Infinity
        else:
            curr_distances[node] = 0

    # calculate min paths to all destinations
    for max_len in range(1, len(graph) + 1):
        tmp_distances = {}
        no_change = True
        for node in graph.all_nodes():
            min_dist = curr_distances[node]
            if debug:
                print(min_dist)
                assert False
            for tail, weight in graph.get_in_edges(node):
                candidate_dist = curr_distances[tail] + weight
                if min_dist > candidate_dist:
                    no_change = False
                    min_dist = candidate_dist
            tmp_distances[node] = min_dist
        if no_change:  # break early if no updates
            break
        assert not no_change and max_len < len(graph), 'Negative Cycle'
        curr_distances = tmp_distances

    return curr_distances


def dijkstra(graph, source):
    """
    Run dijkstra's single source shortest path
    graph must have only positive edge weights
    """
    # initialize heap
    edge_heap = []
    for node, weight in graph.get_out_edges(source):
        edge_heap.append((weight, node))
    heapq.heapify(edge_heap)

    explored = {}
    while(edge_heap):
        weight, node = heapq.heappop(edge_heap)
        if explored.get(node):
            continue
        explored[node] = weight
        for other_node, other_weight in graph.get_out_edges(node):
            if not explored.get(other_node):
                heapq.heappush(edge_heap, (other_weight + weight, other_node))
    return explored


def johnson_apsp(graph, debug=False):
    """
    Calculate all pairs shortest paths for a graph

    Step 1: Add a point S with edges to all nodes O(n)
    Step 2: Run bellman-ford from S O(m*n)
    Step 3: Update all edge weights to be w_n = s_head + w_old - s_tail O(m)
    Step 4: Iteratively run dijkstra shortest path from all nodes O(n*m*log(n))

    If negative cycle exists throws error
    """
    source = 'dummy'
    source_to_original_nodes = {}
    for node in graph.all_nodes():
        source_to_original_nodes[node] = 0
    graph.add_node(source, to_nodes=source_to_original_nodes)

    try:
        s_paths = bellman_ford(graph, source=source, debug=debug)
    except AssertionError:
        raise

    # update weights, delete dummy edges
    graph.del_node(source)
    for node in graph.all_nodes():
        s_tail = s_paths[node]
        for head, edge_weight in graph.get_out_edges(node):
            s_head = s_paths[head]
            graph.update_edge_weight(
                tail=node,
                head=head,
                weight=s_tail + edge_weight - s_head
            )

    short_paths = {}
    for node in graph.all_nodes():
        s_begin = s_paths[node]
        short_paths[node] = dijkstra(graph, node)
        for end, path_len in short_paths[node].items():
            s_end = s_paths[end]
            short_paths[node][end] = path_len - (s_begin - s_end)

    # reset edge weights
    for node in graph.all_nodes():
        s_tail = s_paths[node]
        for head, edge_weight in graph.get_out_edges(node):
            s_head = s_paths[head]
            graph.update_edge_weight(
                tail=node,
                head=head,
                weight=edge_weight - s_tail + s_head
            )

    return short_paths


def floyd_warshall(graph):
    short_paths = {}
    # initializing when no 'interior nodes'
    for start in graph.all_nodes():
        start_short_paths = {}
        start_short_paths[start] = 0
        for node, weight in graph.get_out_edges(start):
            start_short_paths[node] = weight
        short_paths[start] = start_short_paths

    for node_k in graph.all_nodes():
        for start in graph.all_nodes():
            for end in graph.all_nodes():
                start_to_k = short_paths[start].get(node_k, np.Infinity)
                k_to_end = short_paths[node_k].get(end, np.Infinity)
                start_k_end = start_to_k + k_to_end
                if start_k_end < np.Infinity:
                    curr_min_path = short_paths[start].get(end, np.Infinity)
                    short_paths[start][end] = min(start_k_end, curr_min_path)

    # check for negative cycles and remove self paths
    for node in graph.all_nodes():
        assert short_paths[node].pop(node) >= 0, 'Negative Cycle'

    return short_paths


def main():
    # test 1,  4 node graph with a negative edge
    test_graph_1 = Graph(
        [
            ('A', 'B', 2),
            ('A', 'D', 1),
            ('B', 'C', 2),
            ('C', 'D', -4),
        ]
    )
    test1_ans = {
        'A': {'B': 2, 'C': 4, 'D': 0},
        'B': {'C': 2, 'D': -2},
        'C': {'D': -4},
        'D': {},
    }
    test1_res = johnson_apsp(test_graph_1)
    for source in test1_ans:
        assert test1_res.get(source, False) is not False,\
            f' source: {source} not found'
        assert len(test1_ans.get(source)) == len(test1_res.get(source)),\
            'source {source} incorrect'
        for node, dist in test1_ans[source].items():
            assert test1_res.get(source, {}).get(node, {}) == dist,\
                f'source: {source} -> {node} incorrect'

    test1_res_fw = floyd_warshall(test_graph_1)
    for source in test1_ans:
        assert test1_res_fw.get(source, False) is not False,\
            f'F-W source: {source} not found'
        assert len(test1_ans.get(source)) == len(test1_res_fw.get(source)),\
            f'F-W source {source} incorrect'
        for node, dist in test1_ans[source].items():
            assert test1_res_fw.get(source, {}).get(node, {}) == dist,\
                f'F-W source: {source} -> {node} incorrect'
    print('Test 1 Complete')

    # test 2, graph with negative cycle
    test_graph_2 = Graph(
        [
            ('A', 'B', -1),
            ('B', 'C', -1),
            ('C', 'A', -1)
        ]
    )

    try:
        johnson_apsp(test_graph_2)
        assert False, 'Negative cycle not found'
    except AssertionError as e:
        assert str(e) == 'Negative Cycle', 'Johnson Negative cycle not found'

    try:
        floyd_warshall(test_graph_2)
        assert False, 'Negative cycle not found'
    except AssertionError as e:
        assert str(e) == 'Negative Cycle', 'F-W Negative cycle not found'

    print('Test 2 Complete')

    def load_graph(filepath):
        graph = Graph()

        with open(filepath, 'r') as f:
            header = True
            for line in f:
                if header:
                    header = False
                    continue
                tail, head, weight = [int(x) for x in line.split(' ')]
                graph.add_edge(tail, head, weight)

        return graph

    # loading and running graph 1
    file_1 = '/Users/brendonsullivan/Documents/docs/coursera_hw/g1.txt'
    graph_1 = load_graph(file_1)
    try:
        graph_1_apsp = johnson_apsp(graph_1)
    except AssertionError as e:
        if str(e) == 'Negative Cycle':
            print('Graph 1 has a negative cycle')
            graph_1_apsp = {}
        else:
            raise
    print("Graph 1 APSP Complete")

    # loading and running graph 2
    file_2 = '/Users/brendonsullivan/Documents/docs/coursera_hw/g2.txt'
    graph_2 = load_graph(file_2)
    try:
        graph_2_apsp = johnson_apsp(graph_2)
    except AssertionError as e:
        if str(e) == 'Negative Cycle':
            print('Graph 2 has a negative cycle')
            graph_2_apsp = {}
        else:
            raise
    print("Graph 2 APSP Complete")

    # loading and running graph 3
    file_3 = '/Users/brendonsullivan/Documents/docs/coursera_hw/g3.txt'
    graph_3 = load_graph(file_3)
    try:
        graph_3_apsp = floyd_warshall(graph_3)
    except AssertionError as e:
        if str(e) == 'Negative Cycle':
            print('Graph 3 has a negative cycle')
            graph_3_apsp = {}
        else:
            raise
    print("Graph 3 APSP Complete")

    min_path = np.Infinity
    for apsp in [graph_1_apsp, graph_2_apsp, graph_3_apsp]:
        for source, paths in apsp.items():
            for terminus, length in paths.items():
                if length < min_path:
                    min_path = length

    print(f'Shortest path has length {min_path}')


if __name__ == '__main__':
    main()
