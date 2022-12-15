class event:
    def __init__(self):
        self.subscribers = []
        pass

    def subscribe(self, action):
        self.subscribers.append(action)

    def invoke(self, *args):
        for i in self.subscribers:
            i(*args)
