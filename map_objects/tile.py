class Tile:
    """
    A tile on a map, can block movement and/or vision
    """

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # Default to block vision if block movement
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
