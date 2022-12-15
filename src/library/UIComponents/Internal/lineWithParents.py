import pygame


def calcStartPosition(parentA, self):
    self.x = parentA.x
    self.y = parentA.y


def calcEndPosition(parentB, self):
    self.xEnd = parentB.x
    self.yEnd = parentB.y