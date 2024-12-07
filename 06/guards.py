import sys


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
        self.unique = 0
        self.guard = '^'

        self.__load(io)

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
                    print(f"Guard at {self.curpos} facing {self.guard}")
            l += 1

    # walk until we bump into something
    def onepass(self) -> bool:
        # already exited, don't try
        if self.exited:
            return True

        while True:
            # move
            if self.guardroom[self.curpos[0]][self.curpos[1]] != 'X':
                self.guardroom[self.curpos[0]][self.curpos[1]] = 'X'
                self.unique += 1
            prevpos = self.curpos
            self.curpos = (self.curpos[0] + self.dir[0], self.curpos[1] + self.dir[1])
            # check if we're out of bounds
            if self.curpos[0] < 0 or self.curpos[0] >= len(self.guardroom) or self.curpos[1] < 0 or self.curpos[1] >= len(self.guardroom[self.curpos[0]]):
                print(f"Exited at {self.curpos}")
                self.exited = True
                return True
            # check if we're on a wall
            if self.guardroom[self.curpos[0]][self.curpos[1]] == '#':
                self.curpos = prevpos
                break

        # we always turn right, maybe a later puzzle will have us turn differently
        self.guard = newguard(self.guard)
        self.dir = getdir(self.guard)
        print(f"Guard at {self.curpos} facing {self.guard}")
        return False

    def solve(self):
        while not self.onepass():
            pass

    def print(self):
        for line in self.guardroom:
            print(''.join(line))


if __name__ == '__main__':
    guardroom = GuardRoom(sys.stdin)

    print(guardroom.guardroom)
    guardroom.solve()
    guardroom.print()
    print(guardroom.unique)