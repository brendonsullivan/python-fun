"""
1 million integers, both positive and negative
(there might be some repetitions!)
Compute the number of target values t in the interval [-10000,10000]
(inclusive) such that there are distinct numbers x,y
x,y in the input file that satisfy x+y=t
"""


def twoSum(num_array, target, num_lookup):
    lookup = num_lookup
    i = 0
    while(i < len(num_array)):
        val = num_array[i]
        other_val = target - val
        other_val_exists = lookup.get(other_val, False)
        if other_val_exists and other_val != val:
            return True
        else:
            i += 1
    return False


def numTwoSum(num_array, target_array, num_lookup):
    num = 0
    for t in target_array:
        if twoSum(num_array, t, num_lookup):
            num += 1
        if t % 1000 == 0:
            print(t)
    return num


def main():
    data = "/Users/brendonsullivan/Documents/docs/coursera_hw/two_sum.txt"
    targets = [i for i in range(-10000, 10000 + 1)]
    lookup = {}
    nums = []
    with open(data, 'r') as f:
        for line in f:
            nums.append(int(line))
            lookup[int(line)] = True
    print(
        numTwoSum(
            num_array=nums,
            target_array=targets,
            num_lookup=lookup,
            ))


if __name__ == '__main__':
    main()
