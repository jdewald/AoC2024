
import sys
from typing import Optional, Tuple


class Region:

    perim: int

    def __init__(self, name: str, start: Tuple[int,int]):
        self.name = name
        self.perim = 0
        self.items = set()

        self.items.add(start)

    def area(self) -> int:
        return len(self.items)

    def add(self, pt):
        self.items.add(pt)


def visit(cur_pos: Tuple[int,int], cur_region: Region, data: list[list[str]], region_map: dict[Tuple[int,int], Region], to_visit: set[Tuple[int,int]]):
    if cur_pos in region_map:
        return

    if cur_pos[0] < 0 or cur_pos[1] < 0:
        return
    if cur_pos[0] >= len(data) or cur_pos[1] > len(data[0]):
        return

    region_map[cur_pos] = cur_region
    # if we're here, we're still building this particular region
    for add in ([-1,0], [1,0], [0,-1], [0,1]):
        (x , y) = add
        if cur_pos[0] + x < 0 or cur_pos[0] + x >= len(data):
            cur_region.perim += 1
            continue
        if cur_pos[1] + y < 0 or cur_pos[1] + y >= len(data[0]):
            cur_region.perim += 1
            continue
        
        pt = (cur_pos[0]+x, cur_pos[1]+y)
        el = data[pt[0]][pt[1]]
        if el != cur_region.name:
            # found a boundary
            cur_region.perim += 1
            if pt not in region_map:
                to_visit.add(pt)
        else:
            cur_region.add(pt)
            visit(pt, cur_region, data, region_map, to_visit)


# Use a sort of "water-filling" method to populate regions
def find_regions(data: list[list[str]]) -> list[Region]:
    to_visit = set()
    region_map = dict()
    cur_pos = (0,0)
    to_visit.add(cur_pos)
    regions = list()

    while len(to_visit):
        pt = to_visit.pop()

        if pt in region_map:
            continue

        el = data[pt[0]][pt[1]]
        region = Region(el, pt)
        regions.append(region)
        visit(pt, region, data, region_map, to_visit)

    return regions


if __name__ == '__main__':
    data = []
    for line in sys.stdin:
        data.append(list(line.strip()))

    regions = find_regions(data)

    total = 0
    for region in regions:
        print(f'{region.name} A:{region.area()} P:{region.perim} C:{region.area() * region.perim}')
        total += (region.area() * region.perim)

    print(total)
        