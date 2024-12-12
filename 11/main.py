import sys

from more_itertools import flatten

"""
Rules:
- If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
- If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. 
        The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. 
        (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
- If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.


How many stones after 25 blinks
"""

"""
Observations:
It's a sort of fractal... ?
1. The only time we increase our count is if the digits is even
2. Stones that are a 0 go 
    0,1,2024,20 24,2 0 2 4,
    4048 (1..) 4048 8096,
    40 48 (...) 40 48 80 96,
    4 0 (1..) 4 0 4 8 8 0 9 6,
    (4...) (2024...) (4...) (1...) (4...) 16192 16192 (1...) 18216 12144
    (4...) (2024...) (4...) (1...) (4...) 32772608 32772608 (1...) 36869184 24579456
    (4...) (2024...) (4...) (1...) (4...) 3227 2608 3277 2608 (1..) 3686 9184 2457 9456
    (4...) (2024...) (4...) (1...) (4...) 32 27 26 08 32 77 26 08 (1..) 36 86 91 84 24 57 94 56
    (4...) (2024...) (4...) (1...) (4...) 3 2 2 7 2 6 0 8 3 2 7 7 2 6 0 8 (1..) 3 6 8 6 9 1 8 4 2 4 5 7 9 4 5 6
    0 -> 1
    1 -> 2024 -> 20 24 -> 2 0 2 4
    2 -> 4048 -> 40 48 -> 4 0 4 8
    3 -> 6072 -> 60 72 -> 6 0 7 2
    4 (1) -> 8096 (1) -> 80 96 (1) -> 8 0 9 6 (4)
    5 -> 10120 -> 20482880 -> 2048 2880 -> 20 48 28 80 -> 2 0 4 8 2 8 8 0
    6 -> 12144 -> 24579456 -> 2457 9456 -> 24 57 94 56 -> 2 4 5 7 9 4 5 6
    7 -> 14168 -> 28676032 -> 2867 6032 -> 28 67 60 32 -> 2 8 6 7 6 0 3 2
    8 -> 16192 -> 32772608 -> 3277 2608 -> 32 77 26 08 -> 3 2 7 7 2 6 0 8
    9 (1) -> 18216 (1) -> 36869184 (1) -> 3686 9184 (2) -> 36 86 91 84 (4) -> 3 6 8 6 9 1 8 4 (8)

Really the only thing that varies is how fast initial values split as once they split we know what they'll do

So I think it's a matter of:
1. Taking each number in the initial input
2. Work it through until it splits down into individual digits
3. Profit.

Interestingly it turns out that digits 1-4 and 5-9 have the same counts.
They then "map" to the next level. 

"""

value_cache: dict[int, list[int]] = {}

count_cache = {}

# brute force method
def rule(x: int) -> list[int]:
    if x in value_cache:
        return value_cache[x]

    digits = str(x)
    if x == 0:
        value_cache[x] = [1]
    elif len(digits) % 2 == 0:
        value_cache[x] = [
            int(digits[0:int(len(digits)/2)]),
            int(digits[int(len(digits)/2):])
            ]

    else:
        value_cache[x] = [x * 2024]

    return value_cache[x]

def step(data:list[int]) -> list[int]:
    new_stones = list(flatten([rule(x) for x in data]))
    return new_stones

def steps(data:list[int], iters:int) -> list[int]:
    for i in range(iters):
        data = step(data)
        print(len(data))
        print(data)

    return data

def number_step_count(number: int, iters: int) -> int:
    if iters == 0:
        return 1
    next_items = rule(number)
    count = 0
    # because it's cyclical, we can cache the count we saw
    # for a given iteration count and just re-use that without having
    # to navigate
    for item in next_items:
        if (item, iters) not in count_cache:
            that = number_step_count(item, iters-1)
            count_cache[(item, iters)] = that
        count += count_cache[(item, iters)]
        
    return count

def step_count(data: list[int], iters: int) -> int:
    count = 0
    for item in data:
        count += number_step_count(item, iters)
    return count

# 55312
if __name__ == "__main__":
    input = [int(x) for x in sys.stdin.readline().split(" ")]
    print(input)
    iters = int(sys.argv[1])

#    result = steps(input, iters)
#    print(len(result))
    result = step_count(input, iters)
    print(result)
