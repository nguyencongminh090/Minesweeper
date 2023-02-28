import math
import random
import os

"""
Developer NCM
"""


def valid(x, y, w, h,) -> bool:
    return x in range(w) and y in range(h)


# noinspection PyTypeChecker
class Board:
    def __init__(self, width, height, mapBoard):
        self.__width = width
        self.__height = height
        self.__board = [[None] * width for _ in range(self.__height)]
        self.__map = mapBoard
        self.__numWLength = int(math.log10(self.__width)) + 1 if int(math.log10(self.__width)) + 1 > 3 else 3
        self.__numHLength = int(math.log10(self.__height)) + 1

    def display(self):
        # interp.
        # 0 = Empty
        # Natural [1... 10] =  Number of mine
        # -1 = Mine
        for y in range(self.__height):
            text = []
            for x in range(self.__width):
                if self.__board[y][x] is None:
                    text.append(' . '.center(self.__numWLength))
                elif self.__board[y][x] == -2:
                    text.append('F'.center(self.__numWLength))
                elif self.isNumber(x, y):
                    text.append(str(self.__map[y][x]).center(self.__numWLength))
                elif self.isEmpty(x, y):
                    text.append('   '.center(self.__numWLength))
                elif self.isMine(x, y):
                    text.append(' Q '.center(self.__numWLength))
            text = f"{''.join(text)} {y}"
            print(text)
        print(''.join([str(i).center(self.__numWLength) for i in range(self.__width)]))

    def isNumber(self, x, y):
        return self.__map[y][x] in range(1, 9)

    def isEmpty(self, x, y):
        return self.__map[y][x] == 0

    def isMine(self, x, y):
        return self.__map[y][x] == -1

    def expand(self, x, y):
        pattern = [(-1, 0), (-1, 1), (0, 1), (1, 0), (0, -1)]
        if self.isEmpty(x, y):
            self.__board[y][x] = self.__map[y][x]
        elif self.isNumber(x, y):
            self.__board[y][x] = self.__map[y][x]
            return
        else:
            return
        for i, j in pattern:
            if not valid(x + i, y + j, self.__width, self.__height):
                continue
            if self.__board[y + j][x + i] is None:
                self.expand(x + i, y + j)

    def flag(self, x, y):
        self.__board[y][x] = -2

    def showMine(self):
        for x, y in self.__map.listMine:
            self.__board[y][x] = -1


class Map:
    def __init__(self, width, height):
        self.__map = [[0] * width for _ in range(height)]
        self.__width = width
        self.__height = height
        self.listMine = []

    def __getitem__(self, n):
        return self.__map[n]

    def __generateMine(self):
        num_of_mine = int(self.__width * self.__height * 10 / 100)
        num = 0
        while num < num_of_mine:
            pos = (random.randint(0, self.__width - 1), random.randint(0, self.__height - 1))
            if self.__map[pos[1]][pos[0]] == 0:
                self.__map[pos[1]][pos[0]] = -1
                self.listMine.append(pos)
                num += 1
            else:
                continue

    def __generateNumber(self, x, y):
        pattern = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

        def countMine(x2, y2):
            count = 0
            for i, j in pattern:
                if not valid(x2 + i, y2 + j, self.__width, self.__height):
                    continue
                if self.__map[y2 + j][x2 + i] == -1:
                    count += 1
            return count
        for x1, y1 in pattern:
            if valid(x + x1, y + y1, self.__width, self.__height) and \
                    self.__map[y + y1][x + x1] == 0:
                self.__map[y + y1][x + x1] = countMine(x + x1, y + y1)

    def generate(self):
        self.__generateMine()
        for x, y in self.listMine:
            self.__generateNumber(x, y)


class Command:
    def __init__(self, width, height):
        self.mapB = Map(width, height)
        self.mapB.generate()
        self.board = Board(width, height, self.mapB)
        self.width = width
        self.height = height
        self.state = True

    def __setFlag(self, x, y):
        self.board.flag(x, y)
        if (x, y) in self.mapB.listMine:
            self.mapB.listMine.remove((x, y))

    def __expand(self, x, y):
        self.board.expand(x, y)

    def __checkMinePos(self, x, y):
        return (x, y) in self.mapB.listMine

    def __showMine(self):
        self.board.showMine()

    def winCheck(self):
        return len(self.mapB.listMine) == 0

    def command(self, text: str):
        # <option> <x> <y>
        text = text.strip().split()
        if len(text) < 3:
            print("Wrong Syntax ('<option> <x> <y>')")
            input()
        elif text[0].lower() == 'f':
            self.__setFlag(int(text[1]), int(text[2]))
        elif text[0].lower() == 'e':
            if not valid(int(text[1]), int(text[2]), self.width, self.height):
                print('Wrong Coord')
                input()
            elif not self.__checkMinePos(int(text[1]), int(text[2])):
                self.__expand(int(text[1]), int(text[2]))
            else:
                self.__showMine()
                self.state = False
                print('You Lose')
        if self.winCheck():
            self.state = False
            print('You Win')

    def display(self):
        self.board.display()


def main():
    command = Command(int(input('Width: ')), int(input('Height: ')))
    while command.state:
        os.system('cls')
        command.display()
        getInput = input('Input: ')
        command.command(getInput)
        command.display()
    input('Press any key to exit!')


if __name__ == '__main__':
    main()
