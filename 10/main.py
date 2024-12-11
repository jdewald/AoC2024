
import io
import sys
from typing import Tuple

MAX_LEVEL = 9
START_LEVEL = 0

# This is a pretty perfect linear programming one

def load_topmap(input: io.TextIOBase) -> list[list[int]]:
    return [[int(x) for x in list(line.rstrip())] for line in input.readlines()]

# This returns the reachable max level points along this path
def get_reachable(topo: list[list[int]], start_pos: Tuple[int,int], next_level:int = 0, cache: list[set[Tuple[int,int]]]=None) -> set[Tuple[int,int]]:
    reachable = set()
    if start_pos[0] < 0 or start_pos[1] < 0:
        return reachable
    if start_pos[0] >= len(topo[0]) or start_pos[1] >= len(topo[0]):
        return reachable


    # do we have the reachable set from here cached?
    if topo[start_pos[0]][start_pos[1]] == next_level:
        # now we can check the areas around us to go to the next level
        if next_level == MAX_LEVEL:
            # made it to the top!
            return set([start_pos])
        else:
            cache_pos = (start_pos[0]*len(topo[0])) + start_pos[1] 
            if cache[cache_pos] != None:
                return cache[cache_pos]

            reachable |= get_reachable(topo, (start_pos[0]-1,start_pos[1]), next_level + 1, cache)
            reachable |= get_reachable(topo, (start_pos[0]+1,start_pos[1]), next_level + 1, cache)
            reachable |= get_reachable(topo, (start_pos[0],start_pos[1]-1), next_level + 1, cache)
            reachable |= get_reachable(topo, (start_pos[0],start_pos[1]+1), next_level + 1, cache)

        cache[cache_pos] = reachable

        return cache[cache_pos]
    else:
        return reachable

def get_trailcount(topo: list[list[int]], start_pos: Tuple[int,int], next_level:int = 0, cache: list[int]=None) -> int:
    reachable = 0
    if start_pos[0] < 0 or start_pos[1] < 0:
        return reachable
    if start_pos[0] >= len(topo[0]) or start_pos[1] >= len(topo[0]):
        return reachable

    # do we have the reachable set from here cached?
    if topo[start_pos[0]][start_pos[1]] == next_level:
        # now we can check the areas around us to go to the next level
        if next_level == MAX_LEVEL:
            # made it to the top!
            return 1
        else:
            cache_pos = (start_pos[0]*len(topo[0])) + start_pos[1] 
            if cache[cache_pos] != None:
                return cache[cache_pos]

            reachable += get_trailcount(topo, (start_pos[0]-1,start_pos[1]), next_level + 1, cache)
            reachable += get_trailcount(topo, (start_pos[0]+1,start_pos[1]), next_level + 1, cache)
            reachable += get_trailcount(topo, (start_pos[0],start_pos[1]-1), next_level + 1, cache)
            reachable += get_trailcount(topo, (start_pos[0],start_pos[1]+1), next_level + 1, cache)

        cache[cache_pos] = reachable

        return cache[cache_pos]
    else:
        return reachable

if __name__ == '__main__':
    map = load_topmap(sys.stdin)

    score = 0
    trail_score = 0
    cache = [None] * (len(map) * len(map[0])) 
    countcache = [None] * (len(map) * len(map))
    for row in range(len(map)):
        for col in range(len(map[0])):
            if map[row][col] == START_LEVEL:
                reachable = get_reachable(map, (row, col), 0, cache)
                score += len(reachable)

                trail_score += get_trailcount(map, (row, col), 0, countcache)

    print(score)
    print(trail_score)

