# https://www.studytonight.com/code/python/algo/arithmetic-expression-evaluation-stack.php
# class Equation:
#     def __init__(self, eq):
#         self.equation = eq
#
#     def calc(self, **kwargs):
#         stack = []
#         op = []
#         for i in range(len(self.equation)):
#             ...

import time


def f(x):
    return (3 - 2 * x) * (4 - 2 * x) * x


def find():
    lVal = 0
    hVal = 1.5
    val = (hVal + lVal) / 2
    while True:
        if f((lVal + val) / 2) > f((hVal + val) / 2):
            hVal = val
            val = (hVal + lVal) / 2
        elif f((lVal + val) / 2) < f((hVal + val) / 2):
            lVal = val
            val = (hVal + lVal) / 2
        else:
            return val, f(val)


print(find())
