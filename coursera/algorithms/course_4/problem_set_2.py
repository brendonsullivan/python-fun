"""
The first line indicates the number of cities.
Each city is a point in the plane,
and each subsequent line indicates the x- and y-coordinates of a single city.
The distance between two cities is defined as the Euclidean distance
"""
import numpy as np


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    def __lt__(self, other):
        orig = point(0, 0)
        self_mag = self.dist(orig)
        other_mag = other.dist(orig)
        if self_mag < other_mag:
            return True
        elif self_mag > other_mag:
            return False
        elif self.x < other.x:
            return True
        elif self.x > other.x:
            return False
        elif self.y < other.y:
            return True
        else:
            return False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return int(3*self.x) + int(3*self.y)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'({self.x}, {self.y})'


def combinations(selected, pool, choose):  # super hacky but works?
    assert len(pool) >= choose,\
        f'{choose} greater than number of items to pick from.'

    def combinations_helper(selected, remainder, choose):
        if choose == 0:
            excluded = []
            for item in pool:
                if item not in(selected):
                    excluded.append(item)
            combo = (tuple(sorted(selected)), tuple(sorted(excluded)))
            combos.append(combo)
        else:
            for index, item in enumerate(remainder):
                new_selection = selected + [item]
                new_remainder = remainder[min(len(remainder), index+1):]
                combinations_helper(
                    selected=new_selection,
                    remainder=new_remainder,
                    choose=choose-1,
                )

    combos = []
    remainder = [item for item in pool if item not in(selected)]
    choose = choose - len(selected)

    if choose == 0:  # special case we don't do any selection
        combo = (tuple(sorted(selected)), tuple(sorted(remainder)))
        combos.append(combo)

    else:
        for index, item in enumerate(remainder):
            if index + choose > len(remainder):
                break
            new_selection = selected + [item]
            new_remainder = remainder[index+1:]
            combinations_helper(
                selected=new_selection,
                remainder=new_remainder,
                choose=choose-1
            )

    return combos


def tsp(point_list):
    # initializing with source to source to source path of 0
    source = point_list[0]
    paths = {
        (source,): {},
    }
    for point in point_list:
        if point != source:
            paths[(source, )][point] = np.Infinity
        else:
            paths[(source, )][point] = 0

    # finding optimal path from optimal subpaths
    for set_size in range(2, len(point_list)+1):
        print(f'running set size: {set_size}')
        combos = combinations(
            selected=[source], pool=point_list, choose=set_size)
        for in_path, _ in combos:
            tmp_path = list(in_path)
            paths[in_path] = {}
            for point in tmp_path:
                if point == source:
                    continue
                other_subset = tuple(
                    sorted([i for i in tmp_path if i != point]))
                min_path = np.Infinity
                for prev_point in other_subset:
                    if prev_point == source and set_size > 2:
                        continue
                    path_len = (paths[other_subset][prev_point] +
                                point.dist(prev_point))
                    min_path = min(min_path, path_len)
                paths[in_path][point] = min_path

        # deleting combinations no longer used to keep memory feasible
        clean_combos = combinations(
            selected=[source],
            pool=point_list,
            choose=set_size - 1
        )
        for combo, _ in clean_combos:
            del paths[combo]

    # final loop back to start
    min_loop = np.Infinity
    complete_set = tuple(sorted(point_list))
    for end_point in point_list:
        if end_point == source:
            continue
        loop_len = paths[complete_set][end_point] + source.dist(end_point)
        min_loop = min(min_loop, loop_len)

    return min_loop


def main():
    print('Running TSP Test')
    test_point_list = [
        point(0, 0),
        point(0, 1),
        point(1, 1),
        point(1.5, 0.5),
        point(1, 0),
    ]
    tsp_test = tsp(test_point_list)
    assert int(1000*tsp_test) == 4414
    print('Test complete')

    print('Loading data')
    filepath = '/Users/brendonsullivan/Documents/docs/coursera_hw/tsp.txt'
    point_list = []
    with open(filepath, 'r') as f:
        header = True
        for line in f:
            if header:
                header = False
                continue
            x, y = [float(x) for x in line.split(' ')]
            point_list.append(point(x, y))
    print('Running TSP')
    tsp_soln = tsp(point_list)
    print(f'Solution: {tsp_soln}')


if __name__ == '__main__':
    main()
