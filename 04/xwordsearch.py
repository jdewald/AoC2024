
class XWordSearch():

    def __init__(self, filename, word, pivot):
        self.filename = filename
        self.words = []
        self.grid = []
        self.solution = []
        self.count = 0
        self.pivot = pivot
        if word:
            self.words.append(word)

    def read_file(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line[0] == '#':
                    continue
                elif line[0] == 'W':
                    self.words.append(line.strip())
                else:
                    self.grid.append(list(line.strip()))

    def solve(self):
        for word in self.words:
            # since it's a diagonal, the pivot can't be on the first or last row
            for i in range(1,len(self.grid)-1):
                for j in range(1, len(self.grid[i])-1):
                    if self.grid[i][j] == self.pivot:
                        left = self.search(i-1,j-1, (1,1), word) or self.search(i-1,j-1, (1,1), word[::-1])
                        right = self.search(i-1,j+1, (1,-1), word) or self.search(i-1,j+1, (1,-1), word[::-1])
                        if left and right:
                            self.count += 1
                            if self.debug:
                                self.print_solution()
                                print()
                        self.solution = []

    # we look for the pivot and then when we find it
    # we check around to see our word is present diagonally around
    def search(self, i, j, dir, word):
        if i < 0 or i >= len(self.grid) or j < 0 or j >= len(self.grid[i]):
            return False
        if self.grid[i][j] != word[0]:
            return False
        if len(word) == 1:
            self.solution.append((i, j))
            return True
        if self.search(i + dir[0], j + dir[1], dir, word[1:]):
            self.solution.append((i, j))
            return True
        return False

    def print_solution(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (i, j) in self.solution:
                    print(self.grid[i][j].upper(), end='')
                else:
                    print('.', end='')
            print()

    def print_words(self):
        for word in self.words:
            found = False
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.search(i, j, word):
                        print(word)
                        found = True
                        break
                if found:
                    break

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print('Usage: python xwordsearch.py <filename>')
        sys.exit(1)

    filename = sys.argv[1]
    ws = XWordSearch(filename, "MAS", "A")
    ws.debug = False
    ws.read_file()
    ws.solve()
    ws.print_solution()
    print(ws.count)