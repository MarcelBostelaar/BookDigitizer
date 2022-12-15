class event:
    def __init__(self):
        self.subscribers = []
        self.isPaused = False
        self.backLog = []
        pass

    def subscribe(self, action):
        self.subscribers.append(action)

    def invoke(self, *args):
        if self.isPaused:
            self.backLog.append(args)
        else:
            self.__invoke(args)

    def __invoke(self, args):
        for i in self.subscribers:
            i(*args)

    def pause(self):
        self.isPaused = True

    def unpause(self):
        while len(self.backLog) > 0:
            old = self.backLog[0]
            self.backLog.pop(0)
            self.__invoke(old)
        self.isPaused = False
