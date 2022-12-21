from src.library.UIComponents.Internal.UIClass import UIElement
from src.library.UIComponents.Internal.childElementsComponent import addChildFunctionality, drawContained
from src.library.UIComponents.Internal.draggable import makeDraggable
from src.library.UIComponents.Internal.generalUI import drawRectangle, RED


def __centerDivide(self):
    self.dividePosition = self.width/2 - self.divideWidth/2


def __UISubScreen():
    group = UIElement()
    addChildFunctionality(group)
    group.onDraw.subscribe(drawContained)
    return group


def __draggableDivide():
    group = UIElement()
    makeDraggable(group)
    group.onDraw.subscribe(drawRectangle)
    return group


def leftRightSplitScreen():
    """
    A left-right split screen with draggable center.
    .left and .right contain UI parent elements which can hold children to draw in them
    Extra Properties: divideColor, divideWidth, left, right.
    Methods: centerDivide() -> centers the divide
    """
    group = UIElement()
    group.divideColor = RED
    group.divideWidth = 10
    group.width = group.divideWidth
    group.centerDivide = __centerDivide

    addChildFunctionality(group)
    group.onDraw.subscribe(drawContained)

    group.left = __UISubScreen()
    group.right = __UISubScreen()
    divide = __draggableDivide()

    group.copyProperty("dividePosition", divide, "x")
    group.constrain("dividePosition", lambda i, group=group: min(i, group.width - group.divideWidth))
    group.constrain("dividePosition", lambda i: max(0, i))
    divide.copyProperty("x", group, "dividePosition")
    divide.constrain("x", lambda i, group=group: min(i, group.width - group.divideWidth))
    divide.constrain("x", lambda i: max(0, i))
    divide.constrain("y", lambda i: 0)

    divide.copyProperty("width", group, "divideWidth")
    divide.copyProperty("color", group, "divideColor")

    group.left.copyProperty("height", group)
    group.right.copyProperty("height", group)
    divide.copyProperty("height", group)

    group.left.copyProperty("width", group, "dividePosition")
    group.right.dependentProperty("width", group, lambda i: i.width - (i.dividePosition + i.divideWidth))
    group.right.dependentProperty("x", group, lambda i: i.dividePosition + i.divideWidth)

    group.addChild(group.left)
    group.addChild(group.right)
    group.addChild(divide)
    return group


