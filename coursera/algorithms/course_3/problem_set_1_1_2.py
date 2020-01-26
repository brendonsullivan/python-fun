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

def greedyDelta()
