import tcod as libtcod
from game_messages import Message

class Item:
	def __init__(self, use_function=None, **kwargs):
		self.use_function = use_function
		self.function_kwargs = kwargs
