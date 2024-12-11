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

# brute force method
def rule(x: int) -> list[int]:
    if x == 0:
        return [1]
    digits = str(x)
    if len(digits) % 2 == 0:
        return [
            int(digits[0:int(len(digits)/2)]),
            int(digits[int(len(digits)/2):])
            ]
    return [x * 2024]

def step(data:list[int]) -> list[int]:
    new_stones = list(flatten([rule(x) for x in data]))
    return new_stones

def steps(data:list[int], iters:int) -> list[int]:
    for i in range(iters):
        data = step(data)
        print(len(data))
        #print(data)

    return data


if __name__ == "__main__":
    input = [int(x) for x in sys.stdin.readline().split(" ")]
    print(input)
    iters = int(sys.argv[1])

    result = steps(input, iters)
    print(len(result))
