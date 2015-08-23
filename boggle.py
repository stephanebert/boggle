__author__ = 'stephan'
import random
import re
import bisect


class Boggle:

    def __init__(self):
        self.cubes = []
        self.size = 4
        self.board = [['' for j in range(self.size)] for i in range(self.size)]
        self.words = []
        random.seed(0)
        # http://www.bananagrammer.com/2013/10/the-boggle-cube-redesign-and-its-effect.html
        self.load_cubes('classic_cubes')
        self.random_board()
        self.load_wordlist('scrabble_dict')
        self.scores = {3:1, 4:1, 5:2, 6:3, 7:5, 8:11, 9:11, 10:11, 11:11, 12:11, 13:11, 14:11, 15:11, 16:11}

    def load_cubes(self, filename):
        f = open(filename, 'r')
        for line in f:
            line = line.rstrip()
            self.cubes.append(line.split(' '))
        f.close()

    def print_cubes(self):
        for cube in self.cubes:
            for side in cube:
                print(side, end=' ')
            print()

    def random_board(self):
        inds = list(range(self.size**2))
        random.shuffle(inds)
        for i in range(self.size**2):
            row, col = divmod(i, self.size)
            self.board[row][col] = self.cubes[inds[i]][random.randrange(6)]

    def print_board(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.board[i][j], end=' ')
            print()

    def load_wordlist(self, filename):
        f = open(filename, 'r')
        lower = re.compile('^[A-Z]{3,}$')
        for line in f:
            if lower.match(line):
                self.words.append(line.rstrip().lower())
        f.close()

    def is_prefix(self, stack):
        string = self.stack_to_string(stack)
        i = bisect.bisect_left(self.words, string)
        if not 0 <= i < len(self.words):
            return False
        return self.words[i].startswith(string)

    def is_word(self, stack):
        string = self.stack_to_string(stack)
        i = bisect.bisect_left(self.words, string)
        if not 0 <= i < len(self.words):
            return False
        return self.words[i] == string

    def stack_to_string(self, stack):
        string = ''
        for cube in stack:
            string += self.board[cube[0]][cube[1]]
        return string.lower()

    def search_helper(self, search_stack):
        if not self.is_prefix(search_stack):
            return
        if self.is_word(search_stack):
            yield self.stack_to_string(search_stack)
        row, col = search_stack[-1]
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if not (i in range(self.size) and j in range(self.size)):
                    continue
                if (i, j) in search_stack:
                    continue
                search_stack.append((i, j))
                yield from self.search_helper(search_stack)
                search_stack.pop()

    def search(self):
        for row in range(self.size):
            for col in range(self.size):
                search_stack = [(row, col)]
                yield from self.search_helper(search_stack)

    def score(self, word):
        return self.scores[len(word)]