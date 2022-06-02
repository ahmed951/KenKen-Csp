from turtle import shape
import csp
import sys

import numpy as np

from itertools import product, permutations

from functools import reduce

from random import random, shuffle, randint, choice



def are_in_same_row_or_col(xy1, xy2):
    return (xy1[0] == xy2[0]) != (xy1[1] == xy2[1])

def conflicting(A, a, B, b):
    for i in range(len(A)):
        for j in range(len(B)):
            mA = A[i]
            mB = B[j]

            ma = a[i]
            mb = b[j]
            if are_in_same_row_or_col(mA, mB) and ma == mb:
                return True
    return False

def satisfies(values, operation, target):
    for p in permutations(values):
        if reduce(operation, p) == target:
            return True

    return False

def do_operation(operator):
    if operator == '+':
        return lambda a, b: a + b
    elif operator == '-':
        return lambda a, b: a - b
    elif operator == '*':
        return lambda a, b: a * b
    elif operator == '/':
        return lambda a, b: a / b
    else:
        return None

def is_adjacent(xy1, xy2):
    pass

def get_domains(size, cages):
    domains = {}
    for cage in cages:
        members, operator, target = cage

        domains[members] = list(product(range(1, size + 1), repeat=len(members)))

        qualifies = lambda values: not conflicting(members, values, members, values) and satisfies(values, do_operation(operator), target)

        domains[members] = list(filter(qualifies, domains[members]))

    return domains

def get_neighbors(cages):

    neighbors = {}
    for members, _, _ in cages:
        neighbors[members] = []

    for A, _, _ in cages:
        for B, _, _ in cages:
            if A != B and B not in neighbors[A]:
                if conflicting(A, [-1] * len(A), B, [-1] * len(B)):
                    neighbors[A].append(B)
                    neighbors[B].append(A)

    return neighbors

def parse(lines):
    lines = lines.splitlines(True) if isinstance(lines, str) else lines
    content = lines[0][:-1]
    size = int(content)
    #print(lines)
    cages = []
    for line in lines[1:]:
        content = line[:-1]
        if content:
            cages.append(eval(content))
    return size, cages

def generate_puzzle(size):

    board = list(np.zeros((size,size)))
    for i in range(size):
        for j in range(size):
            board[j][i] = ((i + j) % size) + 1

    for i in range(size):
        shuffle(board)

    for c1 in range(size):
        for c2 in range(size):
            rand = random()
            if rand > 0.5:
                for r in range(size):
                    board[r][c1], board[r][c2] = board[r][c2], board[r][c1]


    b = {}
    for i in range(size):
        for j in range(size):
            b[(j + 1, i + 1)] = board[i][j]

    board = b
    uncaged = sorted(board.keys(), key=lambda var: var[1])

    cages = []
    while uncaged:
        cages.append([])
        csize = randint(1, 4)
        cell = uncaged[0]
        uncaged.remove(cell)
        cages[-1].append(cell)
        for _ in range(csize - 1):
            adjs = []
            for other in uncaged:
                if is_adjacent(cell, other):
                    adjs.append(other)
            cell = choice(adjs) if adjs else None
            if not cell:
                break
            uncaged.remove(cell)
            cages[-1].append(cell)
            
        csize = len(cages[-1])
        if csize == 2:
            fst, snd = cages[-1][0], cages[-1][1]
            if board[fst] / board[snd] > 0 and not board[fst] % board[snd]:
                operator = "/" # choice("+-*/")
            else:
                operator = "-" # choice("+-*")
        elif csize == 1:
            cell = cages[-1][0]
            cages[-1] = ((cell, ), '.', board[cell])
            continue
        else:
            operator = choice("+*")
        target = reduce(do_operation(operator), [board[cell] for cell in cages[-1]])
        cages[-1] = (tuple(cages[-1]), operator, int(target))
    return size, cages


def parseGenerateOutput(s,step):
    size , puzzle = generate_puzzle(s)
    a = np.empty((s,s),dtype=object)
    a.fill("")
    rect = []
    colors = ['red','green','blue','cyan','white','yellow','gray','black',"brown","coral","violet","tomato1","snow1","salmon"]
    example = ""
    example += str(size) + "\n"
    for x in puzzle:
        t = x[0][0]
        a[t[0]-1,t[1]-1] = str(x[2]) + (str(x[1]) if (str(x[1]) != ".") else "")
        example += str(x) + "\n"
    i = 0
    for x in puzzle:
        t = x[0]
        #print(t)
        for y in t:
            #print(y,"color = " , colors[i], "value = " , x[2])
            f = y[0]
            s = y[1]
            rect.append(((f-1)*step,(s-1)*step,(f)*step,(s)*step,colors[i]))
        
        i+=1
        if(i >= len(colors)):
            i = 0
    #print(rect)
    a = np.ravel(a).tolist()
    
    #print(a)
    return example ,a,rect

 class KenKen(csp.CSP):
    def __init__(self, size, cages):

        variables = [members for members, _, _ in cages]
        
        domains = get_domains(size, cages)

        neighbors = get_neighbors(cages)

        csp.CSP.__init__(self, variables, domains, neighbors, self.constraint)

        self.size = size

    def constraint(self, A, a, B, b):

        return A == B or not conflicting(A, a, B, b)

    def solve_puzzle(self, size,algo):
        if(algo == "1"):
            soln = csp.backtracking_search(self)
            print("Entered")
        elif(algo == "2"):
            soln = csp.backtracking_search(self, inference=csp.forward_checking)
        elif(algo == "3"):
            soln = csp.backtracking_search(self, inference=csp.mac)

        solution = np.empty((size,size),dtype=object)
        solution.fill("")
        for x in soln:
            for i in range(len(soln[x])):
                t = x[i]
                solution[t[0]-1,t[1]-1] = soln[x][i]
        
        solution = solution.tolist()
        
        return solution         