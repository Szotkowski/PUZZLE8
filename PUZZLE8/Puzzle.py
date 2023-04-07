
from random import randint
from Matrix import Matrix
from queue import PriorityQueue
import random
import pygame

class Puzzle:

    def __init__(self, x, y, width, height, final_state, move, cost, matrix, blocks=[]):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.final_state = final_state
        self.move = move
        self.cost = cost
        self.matrix = matrix
        self.blocks = blocks

    @staticmethod
    def new(x, y, width, height, final_state):
        return Puzzle(x, y, width, height, final_state, [], 0, Matrix(3, 3))

    def validNumbers(self, numbers):
        valid = False
        if len(numbers) == 9:
            ref = list(range(9))
            valid = True
            for i in numbers:
                if int(i) not in ref:
                    valid = False
                else:
                    ref.remove(int(i))
        return valid

    def randomBlocks(self):
        n = randint(30, 40)
        for i in range(n):
            zero = self.matrix.searchBlock(0)
            possibleMoves = []
            if zero[0] > 0:
                possibleMoves.append(self.matrix.moveup)
            if zero[0] < 2:
                possibleMoves.append(self.matrix.movedown)
            if zero[1] > 0:
                possibleMoves.append(self.matrix.moveleft)
            if zero[1] < 2:
                possibleMoves.append(self.matrix.moveright)
            random.choice(possibleMoves)(zero)
        self.setBlocksMatrix()

    def setBlocksMatrix(self):
        blocks = []
        block_x = self.x
        block_y = self.y
        block_w = self.width/3
        block_h = self.height/3
        m = self.matrix.getMatrix()
        i = 0
        for k in range(3):
            for j in range(3):
                blocks.append({'rect': pygame.Rect(block_x, block_y, block_w, block_h), 'block': m[k][j]})
                block_x += block_w+1
                i += 1
            block_y += block_h+1
            block_x = self.x
        self.blocks = blocks

    def setBlocks(self, string):
        numbers = string.split(",")
        blocks = []
        if self.validNumbers(numbers):
            block_x = self.x
            block_y = self.y
            block_w = self.width/3
            block_h = self.height/3
            self.matrix.buildMatrix(string)
            i = 0
            for k in range(3):
                for j in range(3):
                    blocks.append({'rect': pygame.Rect(block_x, block_y, block_w, block_h), 'block': int(numbers[i])})
                    block_x += block_w+1
                    i += 1
                block_y += block_h+1
                block_x = self.x
            self.blocks = blocks
            return True
        return False

    def initialize(self):
        blocks = self.final_state
        self.setBlocks(blocks)

    def existsIn(self, elem, list=[]):
        for item in list:
            if item.isEqual(elem):
                return True
        return False

    def solve(self):
        node = self.matrix
        Mfinal = Matrix(3, 3)
        Mfinal.buildMatrix(self.final_state)
        final = Mfinal.getMatrix()
        queue = PriorityQueue()
        queue.put(node)
        visitedNodes = []
        n = 1

        while (not node.isEqual(final) and not queue.empty()):
            node = queue.get()
            visitedNodes.append(node)
            moves = []
            childNodes = node.getPossibleNodes(moves)
            for i in range(len(childNodes)):
                if not self.existsIn(childNodes[i].getMatrix(), visitedNodes):
                    childNodes[i].move = moves[i]
                    childNodes[i].distance()
                    childNodes[i].setPrevious(node)
                    queue._put(childNodes[i])
            n += 1
        moves = []
        self.cost = n
        if (node.isEqual(final)):
            moves.append(node.move)
            nd = node.previous
            while nd != None:
                if nd.move != '':
                    moves.append(nd.move)
                nd = nd.previous
        return moves