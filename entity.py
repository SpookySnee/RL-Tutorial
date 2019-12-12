import math
import tcod as libtcod
from render_functions import RenderOrder

class Entity:
    """
    Generic entity object
    PC/NPC/etc
    """

    def __init__(self, x, y, char, color, name, blocks=False,fighter=None, render_order = RenderOrder.CORPSE, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self



    def move(self, dx, dy):
        # move Entity given amount
        self.x += dx
        self.y += dy


    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)



    def move_astar(self, target, entities, game_map):
        #create FOV map with dimensions of map
        fov = libtcod.map_new(game_map.width, game_map.height)

        #scan for and mark walls as blocked
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight, not game_map.tiles[x1][y1].blocked)

        #scan all obj to see if they must be navigated around
        #also check obj isn't self or target
        #AI class handles case if self adj to target

        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                #set tile as wall, so will be moved around
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        #Allocate A* path
        # 1.41 is normal cost of diagonal, 0.0 if prohib
        my_path = libtcod.path_new_using_map(fov, 1.41)

        #compute path from self to target
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        #check if path eists, and < 25 tiles
        #path size matters if alt longer paths wanted
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            x, y, = libtcod.path_walk(my_path, True)
            if x or y:
                #set self coord to next tile on path
                self.x = x
                self.y = y
        else:
            #normal move as fallback
            self.move_towards(target.x, target.y, game_map, entities)

        #delete path to free memory
        libtcod.path_delete(my_path)


    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
