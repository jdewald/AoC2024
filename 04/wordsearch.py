
class WordSearch():

    def __init__(self, filename, word=None):
        self.filename = filename
        self.words = []
        self.grid = []
        self.solution = []
        self.count = 0
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
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    for dir in [
                        (0, 1), # right
                        (1, 0), # up
                        (1, 1), # up-right
                        (1, -1), # up-left
                        (-1, 1), # down-right
                        (-1, 0), # down
                        (0,-1), # left
                        (-1, -1) # down-left
                        ]:
                        if self.search(i, j, dir, word):
#                            self.print_solution()
                            print()
#                            self.solution = []
                            self.count += 1

    # We need to be able to handle:
    # forwards
    # backwards
    # up
    # down
    # diagonal
    # overlapping
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
    from wordsearch import WordSearch

    if len(sys.argv) != 2:
        print('Usage: python wordsearch.py <filename>')
        sys.exit(1)

    filename = sys.argv[1]
    ws = WordSearch(filename, "XMAS")
    ws.read_file()
    ws.solve()
    ws.print_solution()
    print(ws.count)