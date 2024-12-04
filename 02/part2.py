import sys
from typing import Tuple

count = 0

# returns whether the data is valid and the index of the first invalid element
def is_valid(data) -> Tuple[bool, int]:
    deltas = [data[i]-data[i-1] for i in range(1, len(data))]

    # can't move too much
    for i in range(len(deltas)):
        if abs(deltas[i]) > 3 or abs(deltas[i]) < 1:
            return False, i+1

    signs = [1 if x > 0 else -1 for x in deltas]

    if abs(sum(signs)) < len(signs):
        first = signs[0]
        for i in range(1, len(signs)):
            if signs[i] != first:
                return False, i+1

    return True, 0

for line in sys.stdin:
    data = [int(x) for x in line.strip().split()]

    (valid, index) = is_valid(data) 
    if valid:
        count += 1
    else:
        # try removing the element or element before

        
        attempts = []
        if index == 2:
            # remote the first item
            attempts.append(("first", data[1:]))

        # remove the item before
        attempts.append(("before", data[0:index-1] + data[index:]))

        # remove the item
        if index < len(data) -1:
            attempts.append(("item", data[0:index] + data[index+1:])) 
        else:
            attempts.append(("item", data[0:index]))

        for (desc, attempt) in attempts:
            if is_valid(attempt)[0]:
                print(f"{data} -> {desc} {attempt}")
                count += 1
                break

print(count)


