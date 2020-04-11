"""
In each instance, the number of variables and the number of clauses is the same, 
and this number is specified on the first line of the file. 
Each subsequent line specifies a clause via its two literals, 
with a number denoting the variable and a "-" sign denoting logical "not"
""" # noqa
import math
import numpy as np


class Clause:
    def __init__(self, var1, condition1, var2, condition2):
        self.clause = {var1: condition1, var2: condition2}
        self.values = {var1: True, var2: True}
        self.var1 = var1
        self.var2 = var2

    def is_satisfied(self):
        v1_sat = self.clause[self.var1] == self.values[self.var1]
        v2_sat = self.clause[self.var2] == self.values[self.var2]

        return v1_sat or v2_sat

    def flip_value(self, var):
        self.values[var] = not self.values[var]

    def get_vars(self):
        return self.var1, self.var2

    def __str__(self):
        cond1 = self.var1 if self.clause[self.var1] else - 1 * self.var1
        cond2 = self.var2 if self.clause[self.var2] else - 1 * self.var2
        val1 = self.var1 if self.values[self.var1] else - 1 * self.var1
        val2 = self.var2 if self.values[self.var2] else - 1 * self.var2

        return f'{cond1} ({val1}) or {cond2} ({val2})'

    def __hash__(self):
        cond1 = self.var1 if self.clause[self.var1] else - 1 * self.var1
        cond2 = self.var2 if self.clause[self.var2] else - 1 * self.var2
        return hash((cond1, cond2))

    def __eq__(self, other):
        if self.var1 == other.var1 and self.var2 == other.var2:
            cond1_eq = self.clause[self.var1] == other.clause[self.var1]
            cond2_eq = self.clause[self.var2] == other.clause[self.var2]
            return cond1_eq and cond2_eq
        return False


class ConditionClauses:
    def __init__(self, clause_list):
        self.var_clause_index = {}
        self.satisfied_clauses = {}
        self.unsatisfied_clauses = {}

        for v1, v2 in clause_list:
            v1_val = True if v1 > 0 else False
            v2_val = True if v2 > 0 else False
            v1 = abs(v1)
            v2 = abs(v2)
            clause = Clause(v1, v1_val, v2, v2_val)
            self.var_clause_index[v1] = self.var_clause_index.get(v1, [])\
                + [clause]
            self.var_clause_index[v2] = self.var_clause_index.get(v2, [])\
                + [clause]
            if clause.is_satisfied():
                self.satisfied_clauses[clause] = True
            else:
                self.unsatisfied_clauses[clause] = True

        self.num_var = len(self.var_clause_index)

    def randomize(self, swap_perc=0.1):
        for val in self.var_clause_index.keys():
            if np.random.random() < swap_perc:
                self.flip_variable(val)

    def get_unsatisifed(self):
        if self.unsatisfied_clauses:
            return next(iter(self.unsatisfied_clauses))
        return None

    def flip_variable(self, val):
        relevant_clauses = self.var_clause_index[val]
        for clause in relevant_clauses:
            clause.flip_value(val)
            if clause.is_satisfied():
                self.unsatisfied_clauses.pop(clause, None)
                self.satisfied_clauses[clause] = True
            else:
                self.satisfied_clauses.pop(clause, None)
                self.unsatisfied_clauses[clause] = True

    def num_vars(self):
        return self.num_var

    def __str__(self):
        satisfied = ',\n'.join([str(i) for i in self.satisfied_clauses.keys()])
        unsatisfied = ',\n'.join(
            [str(i) for i in self.unsatisfied_clauses.keys()])
        return "satisfied:\n" + satisfied + "\nunsatisified:\n" + unsatisfied


def papadimitriou(clauses, is_test=False, max_iter=10**6):
    n = clauses.num_vars()
    for i in range(int(math.log2(n))):
        clauses.randomize()
        for j in range(min(2*n**2, max_iter)):
            un_sat_clause = clauses.get_unsatisifed()
            if un_sat_clause:
                if is_test:
                    print(str(clauses))
                v1, v2 = un_sat_clause.get_vars()
                clauses.flip_variable(np.random.choice([v1, v2]))
            else:
                if is_test:
                    print(str(clauses))
                return True
    return False


def main():
    def load_file(name):
        root_path = '/Users/brendonsullivan/Documents/docs/coursera_hw/'
        clause_list = []
        with open(root_path+name, 'r') as f:
            header = True
            for line in f:
                if header:
                    header = False
                    continue
                cond1, cond2 = [int(x) for x in line.split(' ')]
                clause_list.append((cond1, cond2))
        return ConditionClauses(clause_list)

    is_test = False
    print("Running Test 1")
    test1 = ConditionClauses(
        clause_list=[
            (1, 2),
            (-1, 3),
            (3, 4),
            (4, 2),
        ],
    )
    assert papadimitriou(test1, is_test),\
        'Did not find satisfying when possible'
    print("Test 1 Complete")

    print("Running Test 2")
    test2 = ConditionClauses(
        clause_list=[
            (1, 2),
            (-1, -2),
            (-3, 1),
            (-3, 2),
            (3, -1),
            (3, -2),
        ],
    )
    assert not papadimitriou(test2, is_test),\
        'Found satisfying when impossible'
    print("Test 2 Complete")

    for two_sat in ['2sat1', '2sat2', '2sat3', '2sat4', '2sat5', '2sat6']:
        print(f"Loading {two_sat}")
        sat1_cond = load_file(two_sat+'.txt')
        print(f"Running {two_sat}")
        res = papadimitriou(sat1_cond)
        print(f"{two_sat}: {res}")


if __name__ == '__main__':
    main()
