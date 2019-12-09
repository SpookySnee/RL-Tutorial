class Entity:
    """
    Generic entity object
    PC/NPC/etc
    """

    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        # move Entity given amount
        self.x += dx
        self.y += dy
