from typing import Union

import pygame

from src.debug import debugText, debugText2
from src.library.UIComponents.Internal.UIClass import UIElement
from src.library.UIComponents.Internal.childElementsComponent import addChildFunctionality, \
    resizeWithChildren, drawContained
from src.library.UIComponents.Internal.draggable import makeDraggable
from src.library.UIComponents.Internal.generalUI import RED, BLUE, drawRectangle, GREEN, drawText, BLACK, drawTextNew, \
    textSizeCalculator
from src.library.UIComponents.UIGroup import UIGroup


def __CrossProduct(A):
    X1 = (A[1][0] - A[0][0])
    Y1 = (A[1][1] - A[0][1])
    X2 = (A[2][0] - A[0][0])
    Y2 = (A[2][1] - A[0][1])
    return (X1 * Y2 - Y1 * X2)


def __isConvex(points):
    N = len(points)
    prev = 0
    curr = 0
    for i in range(N):
        temp = [points[i], points[(i + 1) % N],
                points[(i + 2) % N]]
        curr = __CrossProduct(temp)
        if (curr != 0):
            if (curr * prev < 0):
                return False
            else:
                prev = curr
    return True


def __draggableCorner(parent, cornerNumber: Union[str, int]=""):
    group = UIGroup()

    visual = UIElement()
    addChildFunctionality(visual)
    visual.copyProperty("color", parent, "trueCornerColor")
    visual.copyProperty("width", parent, "cornerWidth")
    visual.copyProperty("height", parent, "cornerHeight")
    visual.copyProperty("xTextOffset", parent)
    visual.copyProperty("yTextOffset", parent)
    visual.onDraw.subscribe(drawRectangle)
    makeDraggable(visual)
    visual.anchorAt(UIElement(), "center", 0.5, 0.5)
    group.addChild(visual)
    group.center = visual.center

    text = UIElement()
    text.copyProperty("textColor", parent, "textColor")
    text.copyProperty("fontSize", parent, "fontSize")
    text.onDraw.subscribe(drawTextNew)
    text.text = str(cornerNumber)
    text.dependentProperty("x", visual, lambda i: i.x + i.width + i.xTextOffset)
    text.dependentProperty("y", visual, lambda i: i.yTextOffset)
    text.dependentProperty("width", text, lambda i: textSizeCalculator(i.text, i.fontSize)[0])
    text.dependentProperty("height", text, lambda i: textSizeCalculator(i.text, i.fontSize)[1])
    group.addChild(text)

    return group


def Line(whole, start, end):
    self = UIElement()
    self.dependentProperty("xStart", whole, lambda i: getattr(i, start)[0])
    self.dependentProperty("yStart", whole, lambda i: getattr(i, start)[1])
    self.dependentProperty("xEnd", whole, lambda i: getattr(i, end)[0])
    self.dependentProperty("yEnd", whole, lambda i: getattr(i, end)[1])

    self.dependentProperty("x", self, lambda i: i.xStart if i.xStart < i.xEnd else i.xEnd)
    self.dependentProperty("y", self, lambda i: i.yStart if i.yStart < i.yEnd else i.yEnd)
    self.dependentProperty("width", self, lambda i: abs(i.xStart-i.xEnd))
    self.dependentProperty("height", self, lambda i: abs(i.yStart-i.yEnd))

    self.UITriggerProperties += ["xStart", "yStart", "xEnd", "yEnd"]
    self.copyProperty("color", whole, "trueLineColor")
    self.copyProperty("lineWidth", whole)
    self.onDraw.subscribe(lambda self, surface:
                                 pygame.draw.line(
                                     surface, self.color,
                                     (self.xStart, self.yStart),
                                     (self.xEnd, self.yEnd),
                                     self.lineWidth
                                 ))
    return self


def __centerGetter(corner):
    return corner.x + corner.center.x, corner.y + corner.center.y


def draggableQuadrilateral():
    defaultSize = 200

    whole = UIElement()
    addChildFunctionality(whole)
    whole.onDraw.subscribe(drawContained)
    resizeWithChildren(whole)

    whole.cornerSize = 30
    whole.copyProperty("cornerWidth", whole, "cornerSize")
    whole.copyProperty("cornerHeight", whole, "cornerSize")

    whole.lineColor = BLUE
    whole.lineWidth = 5
    whole.cornerColor = (200, 255, 200, 200)
    whole.errorColor = RED
    whole.dependentProperty("trueLineColor", whole, lambda x: whole.lineColor if x.isConvex else x.errorColor)
    whole.dependentProperty("trueCornerColor", whole, lambda x: whole.cornerColor if x.isConvex else x.errorColor)

    whole.fontSize = 24
    whole.textColor = BLACK
    whole.xTextOffset = 10
    whole.yTextOffset = 10

    corner1 = __draggableCorner(whole, 1)
    whole.dependentProperty("topLeft", corner1, __centerGetter)
    corner2 = __draggableCorner(whole, 2)
    whole.dependentProperty("topRight", corner2, __centerGetter)
    corner3 = __draggableCorner(whole, 3)
    whole.dependentProperty("bottomRight", corner3, __centerGetter)
    corner4 = __draggableCorner(whole, 4)
    whole.dependentProperty("bottomLeft", corner4, __centerGetter)
    corner2.x = defaultSize
    corner3.x = defaultSize
    corner3.y = defaultSize
    corner4.y = defaultSize

    line1 = Line(whole, "topLeft", "topRight")
    line2 = Line(whole, "topRight", "bottomRight")
    line3 = Line(whole, "bottomRight", "bottomLeft")
    line4 = Line(whole, "bottomLeft", "topLeft")

    whole.addChild(line1)
    whole.addChild(line2)
    whole.addChild(line3)
    whole.addChild(line4)

    whole.addChild(corner1)
    whole.addChild(corner2)
    whole.addChild(corner3)
    whole.addChild(corner4)

    whole.dependentProperty("isConvex", whole, lambda x: __isConvex([
        x.topLeft, x.topRight, x.bottomRight, x.bottomLeft
    ]))

    return whole

