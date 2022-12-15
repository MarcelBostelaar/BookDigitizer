from src.library.events import event


class UIElement:
    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onUIChange = event()
        #nothing
        self.drawEvent = event()
        #self, surface
        self.mouseDownEvent = event()
        #self, x, y
        self.mouseUpEvent = event()
        #self, x, y
        self.onTick = event()
        #self
        self.UITriggerProperties = ["x", "y", "width", "height"]
        self.genericTriggers = {}

    def __setattr__(self, name, value):
        if not hasattr(self, name):
            #first time setting
            super().__setattr__(name, value)
            return
        old = self.__getattribute__(name)
        super().__setattr__(name, value)
        if name in self.UITriggerProperties:
            if value != old:
                self.onUIChange.invoke()
        if name in self.genericTriggers.keys():
            self.genericTriggers[name].invoke()

    def subscribeToPropertyTrigger(self, propertyname, func):
        if propertyname not in self.genericTriggers.keys():
            self.genericTriggers[propertyname] = event()
        self.genericTriggers[propertyname].subscribe(func)

    def checkBoundingBox(self, x, y):
        if self.x <= x <= self.width + self.x:
            if self.y <= y <= self.height + self.y:
                return True
        return False

    def checkMouseDown(self, x, y):
        if self.checkBoundingBox(x,y):
            self.mouseDownEvent.invoke(self, x,y)

    def checkMouseUp(self, x, y):
        if self.checkBoundingBox(x,y):
            self.mouseUpEvent.invoke(self, x,y)

    def draw(self, surface):
        self.drawEvent.invoke(self, surface)

    def setAttribute(self, name, value):
        setattr(self, name, value)


