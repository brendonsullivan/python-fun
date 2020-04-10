"""
You should implement the nearest neighbor heuristic:

1. Start the tour at the first city.

2. Repeatedly visit the closest city that the tour hasn't visited yet. In case of a tie, go to the closest city with the lowest index. 
For example, if both the third and fifth cities have the same distance from the first city (and are closer than any other city), 
then the tour should begin by going from the first city to the third city.

3. Once every city has been visited exactly once, return to the first city to complete the tour.
""" # noqa


import numpy as np
from problem_set_2 import point


def approx_tsp(point_list):
    visited = {}
    current_point = point_list[0]
    current_dist = .0
    num_remaining = len(point_list) - 1

    while(num_remaining > 0):
        visited[current_point] = True
        min_dist = np.Infinity
        min_point = None
        for next_point in point_list:
            if visited.get(next_point):
                continue
            dist = current_point.dist(next_point)
            if dist < min_dist:
                min_dist = dist
                min_point = next_point
        current_dist += min_dist
        current_point = min_point
        num_remaining -= 1

    current_dist += current_point.dist(point_list[0])

    return current_dist


def main():
    test = [
        point(0, 0),
        point(0, 1),
        point(1, 1),
        point(1, 0),
    ]

    print("Running Test")
    test_dist = approx_tsp(test)
    assert test_dist == 4.0, f'Test Failed: {test_dist} != 4.0'
    print("Test Complete")

    print("Loading Points")
    point_list = []
    filepath = '/Users/brendonsullivan/Documents/docs/coursera_hw/nn.txt'
    with open(filepath, 'r') as f:
        header = True
        for line in f:
            if header:
                header = False
                continue
            _, x, y = [float(x) for x in line.split(' ')]
            point_list.append(point(x, y))

    print("Running Approx TSP")
    path_dist = approx_tsp(point_list)
    print(f"Result: {path_dist}")


if __name__ == '__main__':
    main()
