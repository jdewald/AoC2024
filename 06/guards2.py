import copy
import sys


# This adds a case where we can try to block the guard. 
# It runs hilariously slowly
# There are definitely optimizations that could happen
def getdir(guard):
    if guard == '^':
        return (-1, 0)
    elif guard == 'v':
        return (1, 0)
    elif guard == '>':
        return (0, 1)
    else:
        return (0, -1)

def newguard(guard):
    if guard == '^':
        return '>'
    elif guard == '>':
        return 'v'
    elif guard == 'v':
        return '<'
    elif guard == '<':
        return '^'

class GuardRoom(object):

    def __init__(self, io):
        self.guardroom = []
        self.curpos = (1, 0)
        self.dir = (1,1)
        self.exited = False
        self.looped = False
        self.unique = 0
        self.guard = '^'
        self.block_pos = set()
        self.block_tried = set()
        self.loop_dir = None
        self.visited = set() 


        self.__load(io)
        self.block_tried.add(self.curpos)

    def reset(self):
        self.guardroom = copy.deepcopy(self._original)
        self.curpos = self._start
        self.dir = self._start_dir
        self.exited = False
        self.looped = False
        self.guard = self._original_guard
        self.unique = self._unique
        self.loop_dir = None
        self.visited = copy.deepcopy(self._visited)

    def save(self):
        self._original = copy.deepcopy(self.guardroom)
        self._start = self.curpos
        self._start_dir = self.dir
        self._original_guard = self.guard
        self._looped = False
        self._exited = False
        self._unique = self.unique
        self._visited = copy.deepcopy(self.visited)

    def __load(self, io):
        self.guardroom = []
        l = 0
        for line in io:
            self.guardroom.append(list(line.strip()))
            # find the guard
            for c in range(len(self.guardroom[l])):
                if self.guardroom[l][c] in ['^', 'v', '<', '>']:
                    self.curpos = (l, c)

                    self.guard = self.guardroom[l][c] 
                    self.dir = getdir(self.guard)
#                    print(f"Guard at {self.curpos} facing {self.guard}")
            l += 1

    # walk until we bump into something
    def onepass(self, with_blocking:bool=False) -> bool:
        # already exited, don't try
        if self.exited:
            return True

        if self.looped:
            return True

        while True:
            # move
            if self.guardroom[self.curpos[0]][self.curpos[1]] != 'X':
                self.guardroom[self.curpos[0]][self.curpos[1]] = 'X'
                self.unique += 1
            prevpos = self.curpos

            newpos = (self.curpos[0] + self.dir[0], self.curpos[1] + self.dir[1])
            if newpos[0] < 0 or newpos[0] >= len(self.guardroom) or newpos[1] < 0 or newpos[1] >= len(self.guardroom[newpos[0]]):
#                print(f"Exited at {self.curpos}")
                self.exited = True
                return True
            if ((self.dir, newpos) in self.visited):
                self.looped = True
                return True

            if with_blocking and newpos not in self.block_tried:
                if self.guardroom[newpos[0]][newpos[1]] == '.':
                    # we can only block if we haven't already visited this position
                    # see if we could instead block from here
                    self.save()
                    self.guardroom[newpos[0]][newpos[1]] = 'O'
                    self.block_tried.add(newpos)
#                    self.guard = newguard(self.guard)
#                    self.dir = getdir(self.guard)
#                    self.print()
                    self.solve(with_blocking=False)
                    if self.looped:
                        self.block_pos.add(newpos)
                    self.reset()

            self.curpos = newpos
            self.visited.add((self.dir, self.curpos))
            # check if we're out of bounds
            # check if we're on a wall
            if self.guardroom[self.curpos[0]][self.curpos[1]] in ['#', 'O']:
                self.curpos = prevpos
                break

        # we always turn right, maybe a later puzzle will have us turn differently
        self.guard = newguard(self.guard)
        self.dir = getdir(self.guard)
#        print(f"Guard at {self.curpos} facing {self.guard}")
        return False

    def solve(self, with_blocking:bool=False):
        while not self.onepass(with_blocking):
            pass

    def print(self):
        for line in self.guardroom:
            print(''.join(line))


if __name__ == '__main__':
    guardroom = GuardRoom(sys.stdin)

    print(guardroom.guardroom)
    guardroom.solve(with_blocking=True)
    guardroom.print()
    print(guardroom.unique)
    print(len(guardroom.block_pos))