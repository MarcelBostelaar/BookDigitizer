import pygame.draw

from src.library import inputs
from src.library.UIComponents.childElementsComponent import addChildFunctionality, resizeWithChildren, drawContained, \
    drawContainedCentered
from src.library.UIComponents.draggable import setDragState, moveObject
from src.library.UIComponents.generalUI import createText, drawCentered, BLACK, RED
from src.library.lineWithParents import calcEndPosition, calcStartPosition
from src.library.uiClasses import UIElement


def identity(origin, x):
    return x


class UIComponentFactory:
    def __init__(self):
        self.operations = []
        self.post = []

    def addOperation(func):
        """Utility decorator to make the builder immutable and reusable without side effects"""
        def wrapper_func(self, *args):
            # Invoke the wrapped function first
            retval = func(self, *args)
            x = UIComponentFactory()
            x.operations = self.operations.copy()
            x.post = self.post.copy()
            x.operations.append(retval)
            return x
        return wrapper_func

    def build(self):
        component = UIElement()
        for i in self.operations:
            i(component)
        for i in self.post:
            i(component)
        return component

    def afterBuild(self, f):
        x = UIComponentFactory()
        x.operations = self.operations.copy()
        x.post = self.post.copy()
        x.post.append(f)
        return x

    @addOperation
    def addChildFunctionality(self):
        return addChildFunctionality

    @addOperation
    def resizeWithChildren(self):
        return resizeWithChildren

    @addOperation
    def drawInternalRegular(self):
        """Draws internal screen on coordinates in the topleft"""
        return lambda x: x.drawEvent.subscribe(drawContained)

    @addOperation
    def drawInternalCentered(self):
        """Draws internal screen centered around the coordinates"""
        return lambda x: x.drawEvent.subscribe(drawContainedCentered)

    @addOperation
    def drawRectangle(self):
        return lambda x: x.drawEvent.subscribe(
            lambda self, surface: pygame.draw.rect(surface, self.color,
                                                                (self.x, self.y, self.width, self.height)
                                                                ))
    @addOperation
    def drawLine(self, parentA, parentB):
        def internal(UIObject):
            parentA.onUIChange.subscribe(lambda a=parentA, self=UIObject: calcStartPosition(a, self))
            parentB.onUIChange.subscribe(lambda b=parentB, self=UIObject: calcEndPosition(b, self))
            UIObject.UITriggerProperties += ["xEnd", "yEnd"]
            UIObject.drawEvent.subscribe(lambda self, surface:
                                         pygame.draw.line(
                                             surface, self.color,
                                             (self.x, self.y),
                                             (self.xEnd, self.yEnd),
                                             self.width
                                         ))
            calcStartPosition(parentA, UIObject)
            calcEndPosition(parentB, UIObject)
        return internal


    @addOperation
    def defaultColor(self, color=RED):
        def internal(x):
            x.color = color
            x.UITriggerProperties += ["color"]
        return internal

    @addOperation
    def defaultTextColor(self, color=BLACK):
        def internal(x):
            x.textcolor = color
            x.UITriggerProperties += ["textcolor"]
        return internal

    @addOperation
    def defaultText(self, text=""):
        def internal(x):
            x.text = text
            x.UITriggerProperties += ["text"]
        return internal

    @addOperation
    def defaultFontSize(self, fontsize=24):
        def internal(x):
            x.fontsize = fontsize
            x.UITriggerProperties += ["fontsize"]
        return internal

    @addOperation
    def copyProperty(self, origin, propertyName):
        def internal(x):
            def internal2():
                setattr(x, propertyName, getattr(origin, propertyName))
            origin.subscribeToPropertyTrigger(propertyName, internal2)
            internal2()
        return internal

    @addOperation
    def dependantProperty(self, origin, propertyNameOnSelf, retriever):
        def internal(x):
            def internal2():
                setattr(x, propertyNameOnSelf, retriever(origin))
            origin.subscribeToPropertyTrigger(propertyNameOnSelf, internal2)
            internal2()
        return internal

    @addOperation
    def drawText(self):
        def internal(UIObject, surface):
            text = createText(UIObject.text, UIObject.width, UIObject.height, UIObject.textcolor, UIObject.fontsize)
            drawCentered(surface, text, UIObject.x, UIObject.y, UIObject.width, UIObject.height)
        return lambda x: x.drawEvent.subscribe(internal)

    @addOperation
    def anchorAt(self, child, xAxisPercentage, yAxisPercentage, name):
        """
        Adds a UIFactory object at an arbitrary anchor point to the item. Parent (this) have children enabled.
        :param xAxisPercentage: float, 0 is left, 1 is right
        :param yAxisPercentage: float, 0 is top, 1 is bottom
        :return:
        """
        def internal(UIObject):
            child.dependantProperty(UIObject, "x", lambda origin: origin.width * xAxisPercentage)
            child.dependantProperty(UIObject, "y", lambda origin: origin.height * yAxisPercentage)
            builded = child.build()
            UIObject.addChild(builded)
            setattr(UIObject, name, builded)
        return internal

    def addAnchorPoint(self, xAxisPercentage, yAxisPercentage, name):
        """
        Adds an arbitrary anchor point (empty UI object) to the item. Must have children enabled.
        :param xAxisPercentage: float, 0 is left, 1 is right
        :param yAxisPercentage: float, 0 is top, 1 is bottom
        :return:
        """
        return self.anchorAt(UIComponentFactory(), xAxisPercentage, yAxisPercentage, name)

    @addOperation
    def makeDraggable(self):
        def internal(UIObject):
            UIObject.isBeingDragged = False
            UIObject.mouseDownEvent.subscribe(setDragState(True))
            # subscribe to global mouse up to prevent accidental sticking when mouse moves too far
            inputs.onMouse1Up.subscribe(lambda x, y, self=UIObject: setDragState(False)(self, x, y))
            UIObject.onTick.subscribe(moveObject)
            UIObject.objectToDrag = UIObject
        return internal


