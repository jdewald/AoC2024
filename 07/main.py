

import sys
from typing import List

OPERATORS = {
    '+': lambda a, b: a + b,
    '*': lambda a, b: a * b,
    '||': lambda a, b: int(str(a) + str(b)), # part2
}

def has_solution(target:int, cur_value: int, data:List[int], chain: List[str]) -> List[str]:
    if len(data) == 0:
        return chain if target == cur_value else []
    if cur_value > target:
        return []

    for op in OPERATORS:
        solution = has_solution(target, OPERATORS[op](cur_value, data[0]), data[1:] if len(data) > 1 else [], chain + [op])
        if solution:
            return solution
    return []

valid = []
for line in sys.stdin:
    (target, vals) = line.strip().split(': ')
    (target, vals) = ((int(target), [int(x) for x in vals.split(' ')]))
    sol = has_solution(target, vals[0], vals[1:], [])
    if sol:
        print((target, vals), sol)
        valid.append((target, vals))

print(sum([v[0] for v in valid]))
