"""
Problem set 1 of coursera algo2 pset.

Has functions for loading scc.txt, loading small test graph
Has class for encapuslating graph and providing methods for graph algos:
    bfs, dfs, scc
"""


def load_file(full_path_name):
    """Load edges from csv and returns adj lists."""
    adj_list = {}
    with open(full_path_name, 'r') as f:
        for line in f:
            source, sink = [int(s) for s in line.strip().split(" ")]
            adj_list[source] = adj_list.get(source, []) + [sink]
    return adj_list


def test_load_file():
    """Load scc file print adj[1]."""
    full_path_name =\
        '/Users/brendonsullivan/Documents/docs/coursera_hw/scc.txt'

    adj_list = load_file(full_path_name)
    print(adj_list[1])


def gen_test_graph():
    """Create test graph with 2 scc and 8 nodes."""
    adj_list = {}
    adj_list[1] = [3]
    adj_list[2] = [1, 5]
    adj_list[3] = [4]
    adj_list[4] = [2, 7]
    adj_list[5] = [7]
    adj_list[6] = [5]
    adj_list[7] = [8]
    adj_list[8] = [6]
    return adj_list


def gen_test_graph_2():
    """Create test graph with 2 scc and 4 nodes."""
    adj_list = {}
    adj_list[1] = [2]
    adj_list[3] = [4]
    return adj_list


class Vertex:
    """Class for encapuslating vertices and properties."""

    def __init__(self, id):
        """Define vertex with given ID."""
        self.id = id
        self.pred = None
        self.explored = False
        self.finish_time = None
        self.source_id = None

    def reset(self):
        """Remove data from vertex."""
        self.pred = None
        self.explored = False
        self.finish_time = None
        self.source_id = None

    def __gt__(self, other):
        """Compare if finished after other."""
        return self.finish_time > other.finish_time

    def __lt__(self, other):
        """Compare if finished before other."""
        return self.finish_time < other.finish_time


class Graph:
    """Class for encapsulating graphs."""

    def __init__(self, adj_list):
        """Build graph from adj_list."""
        self.adj_list = adj_list
        self.vert_list = {}
        self.time = 0
        for id in adj_list.keys():
            self.vert_list[id] = Vertex(id)
            for adj in adj_list[id]:
                self.vert_list[adj] = self.vert_list.get(adj, Vertex(adj))

    def dfs(self, vert_order=None):
        """Run breadth first search."""
        all_vert_ids = vert_order
        if all_vert_ids is None:
            all_vert_ids = self.adj_list.keys()

        for vert_id in all_vert_ids:
            self.vert_list[vert_id].reset()
        self.time = 0

        finish_order = []
        for vert_id in all_vert_ids:
            if self.vert_list[vert_id].explored is False:
                self.vert_list[vert_id].explored = True
                self.vert_list[vert_id].source_id = vert_id
                sub_graph_finish_order = self._dfs_subgraph(vert_id)
                finish_order.extend(sub_graph_finish_order)
        return finish_order

    def _dfs_subgraph(self, source_id):
        """Run dfs on sub graph starting from/connected to source vert."""
        vert_queue = [source_id]
        finish_order = []
        while(len(vert_queue) > 0):
            current_id = vert_queue[-1]
            adj_current = self.adj_list.get(current_id, [])
            all_explored = True
            for vert_id in adj_current:
                vert = self.vert_list[vert_id]
                if vert.explored is False:
                    all_explored = False
                    vert_queue.append(vert_id)
                    vert.explored = True
                    vert.pred = current_id
                    vert.source_id = source_id
                    break
            if all_explored is True:
                vert_id = vert_queue.pop()
                vert = self.vert_list[vert_id]
                vert.finish_time = self.time
                finish_order.append(vert_id)
                self.time += 1
        return finish_order

    def rev_graph(self):
        """Build a reverse version of the graph."""
        rev_adj_list = {}
        for vert_id in self.adj_list.keys():
            for adj_vert_id in self.adj_list[vert_id]:
                rev_adj_list[adj_vert_id] = \
                    rev_adj_list.get(adj_vert_id, []) + [vert_id]
        return Graph(rev_adj_list)

    def scc(self):
        """Caculate strongly connected components of graph."""
        rev = self.rev_graph()
        finish_order = rev.dfs()
        finish_order.reverse()
        self.dfs(finish_order)

    def scc_stats(self):
        """Calculate number of, 5 biggest sizes, and size of each scc."""
        self.scc()
        components = {}
        for vert in self.vert_list.values():
            comp = vert.source_id
            components[comp] = components.get(comp, 0) + 1
        sizes = [val for val in components.values()]
        sizes.sort(reverse=True)

        return len(components), sizes[0:5], components
