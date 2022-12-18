from src.library import inputs


def __setDragState(state):
    def internal(self, x, y):
        self.isBeingDragged = state
    return internal


def __moveObject(self):
    if self.isBeingDragged:
        self.objectToDrag.x += inputs.xMovement
        self.objectToDrag.y += inputs.yMovement


def makeDraggable(UIObject):
    UIObject.isBeingDragged = False
    UIObject.onMouseDown.subscribe(__setDragState(True))
    #subscribe to global mouse up to prevent accidental sticking when mouse moves too far
    inputs.onMouse1Up.subscribe(lambda x, y, self=UIObject: __setDragState(False)(self, x, y))
    UIObject.onTick.subscribe(__moveObject)
    UIObject.objectToDrag = UIObject