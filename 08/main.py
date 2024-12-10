"""
In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - 
but only when one of the antennas is twice as far away as the other.
"""

import math
import sys
from typing import Dict, List, Tuple


def load(io) -> List[List[str]]:
    return [list(line.strip()) for line in io]

def magnitude(vec: Tuple[int,int]) -> float:
    return math.sqrt((vec[0]*vec[0]) + (vec[1]*vec[1]))

def parse_antennas(data: List[List[str]]) -> Dict[str, List[Tuple[int,int]]]:
    antennas = {}

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == '.':
                continue
            if data[i][j] not in antennas:
                antennas[data[i][j]] = []
            antennas[data[i][j]].append((i, j))

    return antennas

def get_antinodes(positions: List[Tuple[int,int]], size: Tuple[int,int], complete:bool=False) -> List[Tuple[int,int]]:
    
    result = []
    for i in range(len(positions)):
        antenna = positions[i]
        for j in range(i+1, len(positions)):
            antenna2 = positions[j]
            if complete:
                result.append(antenna)
                result.append(antenna2)
            original = (antenna2[0]-antenna[0], antenna2[1]-antenna[1])
            mult = 2
            while True:
                added = False
                vec = (original[0]*mult, original[1]*mult)
                # we can go twice as far away by just applying it twice
                antinode = (antenna[0]+(vec[0]),antenna[1]+(vec[1]))
                if antinode[0] >= 0 and antinode[0] < size[0] and antinode[1] >= 0 and antinode[1] < size[1]:
                    result.append(antinode)
                    added = True
                antinode = (antenna2[0]-(vec[0]),antenna2[1]-(vec[1]))
                if antinode[0] >= 0 and antinode[0] < size[0] and antinode[1] >= 0 and antinode[1] < size[1]:
                    result.append(antinode)
                    added = True
                mult+=1
                if not complete:
                    break
                if complete and not added:
                    break

    return result

if __name__ == '__main__':

    grid = load(sys.stdin)
    antennas = parse_antennas(grid)

    size = (len(grid), len(grid[0]))


    unique = set() 

    for freq in antennas:
        print(freq)
        antinodes = get_antinodes(antennas[freq], size)
        for a in antinodes:
            grid[a[0]][a[1]] = '#'
        unique |= set(antinodes)

        for line in grid:
            print(''.join(line))
        print()

    print(len(unique))
    unique = set()
    # part 2
    for freq in antennas:
        print(freq)
        antinodes = get_antinodes(antennas[freq], size, complete=True)
        for a in antinodes:
            grid[a[0]][a[1]] = '#'
        unique |= set(antinodes)

        for line in grid:
            print(''.join(line))
        print()
        

    print(len(unique))

