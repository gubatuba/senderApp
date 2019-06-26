class Message:
    def __init__(self, data):
        self.sender = data.get('sender')
        self.receiver = data.get('receiver')
        self.title = data.get('title')
        self.body = data.get('body')
        self.tile_image = data.
