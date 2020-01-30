"""
Your task is to run Prim's minimum spanning tree algorithm
on this graph. You should report the overall cost of a minimum
spanning tree
"""
import heapq


class Edge:
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def other_node(self, node):
        if node == self.node1:
            return self.node2
        elif node == self.node2:
            return self.node1
        else:
            raise KeyError

    def __lt__(self, other):
        return self.weight < other.weight

    def __gt__(self, other):
        return self.weight > other.weight


class WeightedGraph:
    """Encapsulates graphs, has functions to mark nodes / edges as explored
    """
    def __init__(self):
        self.graph = dict()
        self.explored_edges = dict()
        self.explored_nodes = dict()

    def add_edge(self, node1, node2, weight):
        "Add an edge to the graph"
        new_edge = Edge(node1, node2, weight)
        self.graph[node1] = self.graph.get(node1, []) + [new_edge]
        self.graph[node2] = self.graph.get(node2, []) + [new_edge]

    def mark_node_explored(self, node):
        "Mark a node as explored, note this does not mark an edge as explored"
        self.explored_nodes[node] = True

    def mark_edge_explored(self, edge):
        "Mark an edge explored, note this does not mark either node explored"
        self.explored_edges[edge] = True

    def is_explored_node(self, node):
        return self.explored_nodes.get(node, False)

    def is_explored_edge(self, edge):
        return self.explored_edges.get(edge, False)

    def all_nodes_explored(self):
        return len(self.explored_nodes) == len(self.graph)

    def all_nodes(self):
        return iter(self.graph.keys())

    def get_edges(self, node):
        return self.graph[node]


class EdgeHeap:
    "Implements a min heap of edges (key is the edge weight)"
    def __init__(self):
        self.heap = []

    def add_edge(self, edge):
        heapq.heappush(self.heap, edge)

    def get_min(self):
        return heapq.heappop(self.heap)

    def __len__(self):
        return len(self.heap)


def prim_mst(graph):
    "calculates min span tree of a graph and returns total weight"
    node = next(graph.all_nodes())
    edge_heap = EdgeHeap()
    sum = 0
    while(True):
        graph.mark_node_explored(node)
        for edge in graph.get_edges(node):
            if graph.is_explored_edge(edge):
                continue
            elif graph.is_explored_node(edge.other_node(node)):
                continue
            else:
                graph.mark_edge_explored(edge)
                edge_heap.add_edge(edge)
        if graph.all_nodes_explored():
            break

        while(True):
            next_edge = edge_heap.get_min()
            node1 = next_edge.node1
            node2 = next_edge.node2
            if not graph.is_explored_node(node1):
                sum += next_edge.weight
                node = node1
                break
            elif not graph.is_explored_node(node2):
                sum += next_edge.weight
                node = node2
                break
    return sum


def main():
    data = "/Users/brendonsullivan/Documents/docs/coursera_hw/primm_mst.txt"
    graph = WeightedGraph()
    with open(data, 'r') as f:
        header = True
        for line in f:
            if header:
                header = False
                continue
            node1, node2, weight = [int(x) for x in line.split(' ')]
            graph.add_edge(node1, node2, weight)
    print(prim_mst(graph))


if __name__ == '__main__':
    main()
