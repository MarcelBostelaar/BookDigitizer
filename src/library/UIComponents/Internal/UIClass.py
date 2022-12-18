from src.library.events import event


class callableNone:
    """Special None value"""
    def __init__(self, propertyName):
        self.propertyName = propertyName

    def __call__(self, *args, **kwargs):
        print(f"Missing value '{self.propertyName}' called with args '{args}' and kwargs '{kwargs}'")
        return callableNone(f"Return of ({self.propertyName})")

    def __bool__(self):
        return False


class UIElement:
    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onUIChange = event()
        #nothing
        self.onDraw = event()
        #self, surface
        self.onMouseDown = event()
        #self, x, y
        self.onMouseUp = event()
        #self, x, y
        self.onTick = event()
        #self
        self.UITriggerProperties = ["x", "y", "width", "height"]
        self.genericTriggers = {}
        self.onAnyChange = event()
        self.__initialized = True

    def __setattr__(self, name, value):
        if isinstance(getattr(self, name), callableNone):
            #first time setting
            super().__setattr__(name, value)
            doUpdate = True
        else:
            old = self.__getattribute__(name)
            super().__setattr__(name, value)
            doUpdate = value != old
        if doUpdate and self.__initialized:
            if name in self.UITriggerProperties:
                self.onUIChange.invoke()
            if name in self.genericTriggers.keys():
                self.genericTriggers[name].invoke()
            self.onAnyChange.invoke()

    def __getattr__(self, item):
        return callableNone(item)

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
            self.onMouseDown.invoke(self, x, y)

    def checkMouseUp(self, x, y):
        if self.checkBoundingBox(x,y):
            self.onMouseUp.invoke(self, x, y)

    def draw(self, surface):
        self.onDraw.invoke(self, surface)

    # def setAttribute(self, name, value):
    #     setattr(self, name, value)

    def dependentProperty(self, propertyName: str, origin, propertyGetter: callable):
        def internal():
            setattr(self, propertyName, propertyGetter(origin))
        origin.onAnyChange.subscribe(internal)
        internal()

    def copyProperty(self, propertyName, origin, originPropertyName=None):
        """
        Copies a property from another object and keeps itself updated.
        :param propertyName: The propertyname in self to change.
        :param origin: The place to get the value from
        :param originPropertyName: If none is given, uses propertyName from the origin
        :return:
        """
        if originPropertyName is None:
            originPropertyName = propertyName

        def internal():
            setattr(self, propertyName, getattr(origin, originPropertyName))

        origin.subscribeToPropertyTrigger(originPropertyName, internal)
        internal()

    def anchorAt(self, child, name, xAxisPercentage, yAxisPercentage):
        """Adds a UIFactory object at an arbitrary anchor point to the item. Parent (this) have children enabled.
        :param child: the element to anchor
        :param name: the name at which to anchor it in this
        :param xAxisPercentage: float, 0 is left, 1 is right
        :param yAxisPercentage: float, 0 is top, 1 is bottom"""
        child.dependentProperty("x", self, lambda origin: origin.width * xAxisPercentage)
        child.dependentProperty("y", self, lambda origin: origin.height * yAxisPercentage)
        self.addChild(child)
        setattr(self, name, child)

