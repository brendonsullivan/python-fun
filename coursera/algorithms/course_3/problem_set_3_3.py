"""
Your task in this problem is to run the
dynamic programming algorithm (and the
reconstruction procedure) from lecture
on this data set.

The question is: of the vertices
1, 2, 3, 4, 17, 117, 517, and 997,
which ones belong to the maximum-weight
independent set?

By "vertex 1" we mean the first vertex of
the graph---there is no vertex 0.

In the box below, enter a 8-bit string,
where the ith bit should be 1 if the ith
of these 8 vertices is in the maximum-weight
independent set, and 0 otherwise
"""


def mwis(node_weights):
    w_0 = node_weights[0]
    w_1 = node_weights[1]
    opt_0 = [0]
    opt_1 = [1]
    for node, weight in enumerate(node_weights[2:], 2):
        # case 1 don't include current node
        if w_1 > w_0 + weight:
            w_0 = w_1
            w_1 = w_1
            opt_0 = opt_1
            opt_1 = opt_1
        # case 2 include current node
        else:
            w_tmp = w_1
            w_1 = weight + w_0
            w_0 = w_tmp
            opt_tmp = opt_1
            opt_1 = opt_0 + [node]
            opt_0 = opt_tmp
    return w_1, opt_1


def main():
    data = "/Users/brendonsullivan/Documents/docs/coursera_hw/mwis.txt"
    node_weights = []
    with open(data, 'r') as f:
        for index, line in enumerate(f):
            # skipping header row
            if index == 0:
                continue
            node_weights.append(int(line))
    check_nodes = {
       1: 0,
       2: 0,
       3: 0,
       4: 0,
       17: 0,
       117: 0,
       517: 0,
       997: 0,
    }

    weight, nodes = mwis(node_weights)
    for node in nodes:
        if check_nodes.get(node+1) is not None:
            check_nodes[node+1] = 1

    binary_check = ''
    for node in [1, 2, 3, 4, 17, 117, 517, 997]:
        binary_check += str(check_nodes[node])

    print(binary_check)


if __name__ == '__main__':
    main()
