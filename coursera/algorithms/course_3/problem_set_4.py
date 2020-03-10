"""
This file describes a knapsack instance, and it has the following format:
[knapsack_size][number_of_items]
[value_1] [weight_1]
[value_2] [weight_2]
"""


def knapsack(item_list, max_weight):
    """Calculates value of optimum number of items given
    list of items with values and weights and a maximal pack weight
    """

    # initializing values for no items
    values = [0 for weight in range(max_weight + 1)]

    for item in item_list:
        tmp_values = []  # optimal values w/ current item. replaces values
        value_i = item[0]
        weight_i = item[1]
        for weight in range(max_weight + 1):
            exclude_val = values[weight]
            include_val = -1  # values will always be > 0
            remainder_weight = weight - weight_i
            if remainder_weight >= 0:
                include_val = value_i + values[remainder_weight]
            tmp_values.append(max(exclude_val, include_val))
        values = tmp_values

    return values[-1]


def main():
    test1 = knapsack(
            item_list=[
                [3, 8],
                [4, 7],
                [2, 5]],
            max_weight=12
        )
    assert test1 == 6, 'test 1 failed'
    test2 = knapsack(
            item_list=[
                [3, 8],
                [4, 7],
                [2, 5]],
            max_weight=10
        )
    assert test2 == 4, 'test 2 failed'

    items_1 = []
    max_weight_1 = None
    knapsack_1_file = '/Users/brendonsullivan/Documents/docs/coursera_hw/knapsack_1.txt' # noqa
    with open(knapsack_1_file, 'r') as f:
        header = True
        for line in f:
            if header:
                header = False
                max_weight_1 = int(line.split(' ')[0])
                continue
            value, weight = [int(x) for x in line.split(' ')]
            items_1.append([value, weight])

    print(knapsack(items_1, max_weight_1))

    items_big = []
    max_weight_big = None
    knapsack_big_file = '/Users/brendonsullivan/Documents/docs/coursera_hw/knapsack_big.txt' # noqa
    with open(knapsack_big_file, 'r') as f:
        header = True
        for line in f:
            if header:
                header = False
                max_weight_big = int(line.split(' ')[0])
                continue
            value, weight = [int(x) for x in line.split(' ')]
            items_big.append([value, weight])

    print(knapsack(items_big, max_weight_big))


if __name__ == '__main__':
    main()
