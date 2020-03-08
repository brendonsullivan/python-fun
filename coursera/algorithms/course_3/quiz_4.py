"""
Computation of optimal binary search tree
given search frequencies

Consider an instance of the optimal binary search tree problem
with 7 keys (say 1,2,3,4,5,6,7 in sorted order)
and frequencies w_1 = .05, w_2 = .4, w_3 = .08,
w_4 = .04, w_5 = .1, w_6 = .1, w_7 = .23
"""


def opt_b_tree(weights):
    """Calculates average search time for
    optimal binary search tree given
    array of weights in ascending node value order
    """
    # initialize solns
    # first index is sequence start
    # second index is sequence len
    solutions = []
    num_nodes = len(weights)
    for weight in range(num_nodes):
        solutions.append([0])

    seq_len = 1
    while (seq_len <= num_nodes):
        seq_start = 0
        while(seq_start + seq_len <= num_nodes):
            # constant to add to avg sub search times
            const = 0
            for node in range(seq_start, seq_start + seq_len):
                const += weights[node]

            # search in sequence for optimal b tree root
            min_avg_search = None
            len_left = 0
            len_right = seq_len - 1
            for root in range(seq_start, seq_start + seq_len):
                # if first element init min_avg_search
                left = 0
                right = 0
                if len_left != 0:
                    left = solutions[seq_start][len_left]
                if len_right != 0:
                    right = solutions[root+1][len_right]
                tmp = const + left + right
                if not min_avg_search or min_avg_search > tmp:
                    min_avg_search = tmp
                len_left += 1
                len_right -= 1
            solutions[seq_start].append(min_avg_search)
            seq_start += 1
        seq_len += 1

    return solutions[0][num_nodes]


def main():
    print(
        opt_b_tree([0.1, 0.5])
    )
    print(
        opt_b_tree([.05, .4, .08, .04, .1, .1, .23])
    )


if __name__ == '__main__':
    main()
