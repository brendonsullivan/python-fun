"""
Given stream of intergers between 1 and 10,000
calculate median at each point in stream
return sum of calculated medians modulo 10,000
"""

import heapq


class heapHelper:
    "Wrapper around python heap methods"

    def __init__(self, is_min=True):
        self.heap = []
        self.is_min = is_min
        self.size = 0

    def push(self, val):
        if not self.is_min:
            val *= -1
        heapq.heappush(self.heap, val)
        self.size += 1

    def pop(self):
        if self.size == 0:
            return

        val = heapq.heappop(self.heap)
        if not self.is_min:
            val *= -1
        self.size -= 1
        return val


def main():
    lower_half = heapHelper(is_min=False)
    upper_half = heapHelper(is_min=True)

    data = "/Users/brendonsullivan/Documents/docs/coursera_hw/median.txt"
    median_sum = 0
    with open(data, 'r') as f:
        for line in f:
            val = int(line)
            total_size = lower_half.size + upper_half.size + 1
            upper_lower = lower_half.pop()
            lower_upper = upper_half.pop()
            if upper_lower is None:
                median_sum += val
                lower_half.push(val)
            elif lower_upper is None:
                median = min(val, upper_lower)
                median_sum += median
                upper_half.push(max(val, upper_lower))
                lower_half.push(median)
            else:
                values = sorted([upper_lower, val, lower_upper])
                if total_size % 2 == 0:
                    lower_half.push(values[0])
                    upper_half.push(values[1])
                    upper_half.push(values[2])
                else:
                    lower_half.push(values[0])
                    lower_half.push(values[1])
                    upper_half.push(values[2])
                median = lower_half.pop()
                median_sum += median
                lower_half.push(median)
    print(median_sum % 10000)
    print(lower_half.size)
    print(upper_half.size)
    print(upper_half.pop())
    print(lower_half.pop())


if __name__ == "__main__":
    main()
