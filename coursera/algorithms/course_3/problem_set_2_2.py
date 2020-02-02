"""
two nodes uu and vv in this problem is defined
as the Hamming distance--- the number of differing bits
--- between the two nodes' labels

The question is: what is the largest value of kk such that
 there is a kk-clustering with spacing at least 3? That is,
 how many clusters are needed to ensure that no pair of nodes
 with all but 2 bits in common get split into different clusters?
"""

from problem_set_2_1 import UnionFind


def max_clusters_two_span(nodes):
    clusters = UnionFind(nodes)
    swap = {
        '0': '1',
        '1': '0',
    }
    for node in nodes:
        for i in range(len(node)):
            new_node = \
                node[0:i] +\
                swap[node[i]] +\
                node[i+1:]
            if clusters.find(new_node):
                clusters.union(node, new_node)
            for j in range(i+1, len(node)):
                new_node_2 = \
                    new_node[0:j] +\
                    swap[new_node[j]] + \
                    new_node[j+1:]
                if clusters.find(new_node_2):
                    clusters.union(node, new_node_2)
    return clusters


def main():
    data = "/Users/brendonsullivan/Documents/docs/coursera_hw/cluster_big.txt"
    nodes = []
    with open(data, 'r') as f:
        header = True
        for line in f:
            if header:
                header = False
                continue
            nodes.append(
                line.
                replace(' ', '').
                replace('\n', ''))
    max_clust = max_clusters_two_span(nodes)
    print(max_clust.num_partitions)


if __name__ == '__main__':
    main()
