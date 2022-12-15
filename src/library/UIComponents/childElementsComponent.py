import pygame

from src.library.UIComponents.generalUI import CLEAR


def __recalcSize(self):
    newWidth = 0
    newHeight = 0
    for child in self.children:
        if child.width + child.x > newWidth:
            newWidth = child.width + child.x
        if child.height + child.y > newHeight:
            newHeight = child.height + child.y
    self.width = newWidth
    self.height = newHeight


def __drawChildren(self, surface):
    """
    Draws children to internal surface.
    :param self:
    :param surface:
    :return:
    """
    self.surface.fill(CLEAR)
    for child in self.children:
        child.draw(self.surface)


def __onMouseDown(self, x, y):
    for child in self.children:
        child.checkMouseDown(x - self.x, y - self.y)


def __onMouseUp(self, x, y):
    for child in self.children:
        child.checkMouseUp(x - self.x, y - self.y)


def __onTick(self):
    for child in self.children:
        child.onTick.invoke(child)


def __addChild(self, child):
    self.children.append(child)


def __addChildResize(self, child):
    self.children.append(child)
    child.onUIChange.subscribe(lambda self=self: __recalcSize(self))
    __recalcSize(self)


# Below are


def drawContained(self, surface):
    """Draws internal surface to screen at x y"""
    surface.blit(self.surface, (self.x, self.y))


def drawContainedCentered(self, surface):
    """Draws internal surface to screen centered around x y"""
    surface.blit(self.surface, (self.x - self.width/2, self.y - self.height/2))


def addChildFunctionality(UIObject):
    """
    Turns object into a child having object. Makes children draw to internal surface. Does not by default draw self.
    :param UIObject:
    :return:
    """
    UIObject.children = []
    UIObject.addChild = lambda child, self=UIObject: __addChild(self, child)
    UIObject.drawEvent.subscribe(__drawChildren)
    UIObject.mouseDownEvent.subscribe(__onMouseDown)
    UIObject.mouseUpEvent.subscribe(__onMouseUp)
    UIObject.onTick.subscribe(__onTick)

    def updateSurfaceSize(self):
        self.surface = pygame.Surface((UIObject.width, UIObject.height), pygame.SRCALPHA)

    updateSurfaceSize(UIObject)
    UIObject.onUIChange.subscribe(lambda self=UIObject: updateSurfaceSize(self))


def resizeWithChildren(UIObject):
    """
    Makes child having object change its size to fit its children, to prevent cutoff.
    :param UIObject:
    :return:
    """
    UIObject.addChild = lambda child, self=UIObject: __addChildResize(self, child)
    for x in UIObject.children:
        x.onUIChange.subscribe(lambda self=UIObject: __recalcSize(self))
    __recalcSize(UIObject)