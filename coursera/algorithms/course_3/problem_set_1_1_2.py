"""
part 1:

Your task in this problem is to run the greedy
algorithm that schedules jobs in decreasing order of the difference
(weight - length). Recall from lecture that this algorithm
is not always optimal.
IMPORTANT: if two jobs have equal difference (weight - length),
you should schedule the job with higher weight first.
Beware: if you break ties in a different way,
you are likely to get the wrong answer.
You should report the sum of weighted completion times of the
resulting schedule

part 2:

Your task now is to run the greedy algorithm that
schedules jobs (optimally) in decreasing order of the
ratio (weight/length). In this algorithm,
it does not matter how you break ties. You
should report the sum of weighted completion times of the
resulting schedule
"""


class Job:
    "Encapsulates jobs, weights and delta / ratio comparison"
    def __init__(self, weight, length):
        self.weight = weight
        self.length = length

    def getRatio(self):
        return self.weight / self.length

    def getDelta(self):
        return self.weight - self.length


class GreedyOpt:
    "Calculates cost given ordering by w - l"
    def __init__(self, job_list):
        self.job_list = job_list

    def _greater(self, job1, job2, dtype):
        if dtype == 'ratio':
            return self._greaterRatio(job1, job2)
        else:
            return self._greaterDelta(job1, job2)

    def _greaterRatio(self, job1, job2):
        v1 = job1.getRatio()
        v2 = job2.getRatio()
        if v1 > v2:
            return job1
        else:
            return job2

    def _greaterDelta(self, job1, job2):
        v1 = job1.getDelta()
        v2 = job2.getDelta()
        if v1 > v2:
            return job1
        elif v1 < v2:
            return job2
        else:
            if job1.weight > job2.weight:
                return job1
            else:
                return job2

    def _sort(self, lo, hi, dtype):
        if hi <= lo:
            return
        j = self._partition(lo, hi, dtype)
        self._sort(lo, j - 1, dtype)
        self._sort(j + 1, hi, dtype)

    def _partition(self, lo, hi, dtype):
        i = lo
        j = hi + 1
        val = self.job_list[i]
        while(True):
            while(True):  # from right going left
                i += 1
                if self._greater(val, self.job_list[i], dtype) == val:
                    break
                if i == hi:
                    break
            while(True):  # from left going right
                j -= 1
                if self._greater(val, self.job_list[j], dtype) != val:
                    break
                if j == lo:
                    break
            if i >= j:
                break
            temp = self.job_list[i]
            self.job_list[i] = self.job_list[j]
            self.job_list[j] = temp
        self.job_list[lo] = self.job_list[j]
        self.job_list[j] = val
        return j

    def cost(self, dtype):
        self._sort(0, len(self.job_list) - 1, dtype)
        sum = 0
        time = 0
        for job in self.job_list:
            time += job.length
            sum += time * job.weight
        return sum


def main():
    data = "/Users/brendonsullivan/Documents/docs/coursera_hw/jobs.txt"
    job_list = []
    with open(data, 'r') as f:
        header = True
        for line in f:
            if header:
                header = False
                continue
            weight, length = line.split(' ')
            job_list.append(Job(int(weight), int(length)))

    g = GreedyOpt(job_list)
    print(g.cost('delta'))
    print(g.cost('ratio'))


if __name__ == '__main__':
    main()
