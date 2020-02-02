"""
Your task in this problem is to run the clustering algorithm
from lecture on this data set, where the target number k of
clusters is set to 4. What is the maximum spacing of a 4-clustering?
"""


class Edge:
    def __init__(self, node1, node2, dist):
        self.node1 = node1
        self.node2 = node2
        self.dist = dist

    def get_other(self, node):
        if node == self.node1:
            return self.node2
        elif node == self.node2:
            return self.node1
        else:
            raise ValueError

    def get_both(self):
        return self.node1, self.node2

    def __lt__(self, other):
        return self.dist < other.dist

    def __gt__(self, other):
        return self.dist > other.dist


class UnionFind:
    def __init__(self, items):
        "Initialize where each item is a separate partition"
        self.item_to_partition = dict(zip(items, items))
        self.partition_contents = dict(zip(items, [[item] for item in items]))
        self.num_partitions = len(self.partition_contents)

    def find(self, item):
        "Return what partition an item is in"
        return self.item_to_partition.get(item)

    def union(self, item1, item2):
        "Union two items by merging containing partitions)"
        partition_1 = self.find(item1)
        partition_2 = self.find(item2)
        if partition_1 == partition_2:
            return

        len_1 = len(self.partition_contents[partition_1])
        len_2 = len(self.partition_contents[partition_2])
        if len_1 > len_2:
            items_2 = self.partition_contents.pop(partition_2)
            self.partition_contents[partition_1].extend(items_2)
            for item in items_2:
                self.item_to_partition[item] = partition_1
            self.num_partitions -= 1
        else:
            items_1 = self.partition_contents.pop(partition_1)
            self.partition_contents[partition_2].extend(items_1)
            for item in items_1:
                self.item_to_partition[item] = partition_2
            self.num_partitions -= 1


def cluster_min_span(items, distance_pairs, num_clust=4):
    """
    Calculates min span for items given their distances
    and number of clusters. Assumes distance_pairs are edges
    """
    clusters = UnionFind(items)
    distance_pairs.sort()
    for pair in distance_pairs:
        p, q = pair.get_both()
        if clusters.find(p) == clusters.find(q):
            continue
        elif clusters.num_partitions == num_clust:
            return pair.dist
        else:
            clusters.union(p, q)


def main():
    data = "/Users/brendonsullivan/Documents/docs/coursera_hw/clustering1.txt"
    nodes = []
    dist_pairs = []
    with open(data, 'r') as f:
        header = True
        for line in f:
            if header:
                header = False
                continue
            p, q, dist = [int(x) for x in line.split(' ')]
            nodes.extend([p, q])
            dist_pairs.append(Edge(p, q, dist))
    print(
        cluster_min_span(
            items=nodes,
            distance_pairs=dist_pairs,
            num_clust=4))


if __name__ == '__main__':
    main()
