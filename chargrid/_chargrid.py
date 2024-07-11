import random
from typing import Any, Union, Type
from CharActor import create, character_bank
from CharActor._charactor.actor._actor.base_actor import BaseCharacter as _BaseCharacter
from CharTask import task_list as _task_list
from CharObj import Goods, Armory, Item, ItemStack
from grid_engine import grid as Grid, grid_object as GridObject
from .meta import *
from . import enemy
from .enemy import *




# Let's create a class to hold our game state
# The game state will include the grid and the characters
# We'll also attach the Catalogues, `Goods` and `Armory` to the grid object
# so that the characters can access them easily.

import random
import json
import grid_engine as ge

class Dungeon:
    def __init__(self, width, height, max_rooms, min_room_size, max_room_size):
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
        self.grid = ge.grid.Grid(cell_size=1, dimensions=(width, height), with_terrain=False)
        for cell in self.grid:
            self.grid[cell].passable = False
        self.rooms = []
        self.room_groups = {}
        
    def create_structure(self, x, y, structure):
        self.grid[x, y].passable = True
        return ge.grid_object.GridStructure(self.grid, structure, self.grid[x, y], passable=True)
        
    def create_room(self, x, y, w, h):
        room_count = len(self.rooms)
        room_center = (x + w // 2, y + h // 2)
        room = ge.grid_object.GridZone(self.grid, f'room{room_count+1}', 'area', room_center)
        for j in range(x, x + w):
            for i in range(y, y + h):
                structure = self.create_structure(j, i, 'room')
                cell = self.grid[j, i]
                cell.add_object(structure)
                cell.add_zone(room)
                room._add_cell(cell)
        self.room_groups[room.name] = room
                
    def is_room_valid(self, x, y, w, h):
        if x + w >= self.width or y + h >= self.height:
            return False
        for i in range(x - 1, x + w + 1):
            for j in range(y - 1, y + h + 1):
                if self.grid[i, j].entry_object['structures'] is not None:
                    return False
        return True

    def place_rooms(self):
        for _ in range(self.max_rooms):
            w = random.randint(self.min_room_size, self.max_room_size)
            h = random.randint(self.min_room_size, self.max_room_size)
            x = random.randint(0, self.width - w - 1)
            y = random.randint(0, self.height - h - 1)

            if self.is_room_valid(x, y, w, h):
                self.create_room(x, y, w, h)
                self.rooms.append((x, y, w, h))

    def connect_rooms(self):
        for i in range(len(self.rooms) - 1):
            x1, y1, w1, h1 = self.rooms[i]
            x2, y2, w2, h2 = self.rooms[i + 1]
            cx1, cy1 = x1 + w1 // 2, y1 + h1 // 2
            cx2, cy2 = x2 + w2 // 2, y2 + h2 // 2

            if random.choice([True, False]):
                self.create_h_corridor(cx1, cx2, cy1)
                self.create_v_corridor(cy1, cy2, cx2)
            else:
                self.create_v_corridor(cy1, cy2, cx1)
                self.create_h_corridor(cx1, cx2, cy2)

    def create_h_corridor(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if self.grid[x, y].entry_object['structures'] is None:
                structure = self.create_structure(x, y, 'corridor')
                self.grid[x, y].add_object(structure)

    def create_v_corridor(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if self.grid[x, y].entry_object['structures'] is None:
                structure = self.create_structure(x, y, 'corridor')
                self.grid[x, y].add_object(structure)

                    
    def save_to_json(self, filename):
        data = {
            'width': self.width,
            'height': self.height,
            'max_rooms': self.max_rooms,
            'min_room_size': self.min_room_size,
            'max_room_size': self.max_room_size,
            'grid': self.grid,
            'rooms': self.rooms
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.width = data['width']
        self.height = data['height']
        self.max_rooms = data['max_rooms']
        self.min_room_size = data['min_room_size']
        self.max_room_size = data['max_room_size']
        self.grid = data['grid']
        self.rooms = data['rooms']

    def print_dungeon(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[x, y].entry_object['structures'] is not None:
                    print(' ', end='')
                else:
                    print('#', end='')
            print()


# Parameters for the dungeon

class Game:
    _grid = None
    _characters = None
    _player = None
    _enemy = None
    _task_list = None

    @property
    def grid(self) -> Type[Grid.Grid]:
        return self._grid
    
    @grid.setter
    def grid(self, grid: Type[Grid.Grid]) -> None:
        self._grid = grid
        
    @property
    def characters(self) -> list:
        if self._characters is None:
            self._characters = []
        return self._characters
    
    @characters.setter
    def characters(self, characters: list) -> None:
        if self._characters is None:
            self._characters = []
        self._chaaracters = characters
        
    @property
    def player(self) -> _BaseCharacter:
        return self._player        

    @player.setter
    def player(self, player: _BaseCharacter):
        self._player = player

    @property
    def enemy(self) -> _BaseCharacter:
        return self._enemy
    
    @enemy.setter
    def enemy(self, enemy: _BaseCharacter):
        self._enemy = enemy

    @property
    def task_list(self) -> list:
        return self._task_list
    
    @task_list.setter
    def task_list(self, task_list: list) -> None:
        self._task_list = task_list
        
    def __init__(self, map_type: str = 'land', dimensions: tuple = (540, 460)):
        print('Generating grid...')
        if map_type == 'land':
            self.grid = ge.grid.Grid(cell_size=2, dimensions=dimensions, with_terrain=False)
        elif map_type == 'dungeon':
            self.dungeon = Dungeon(*dimensions, 20, 10, 20)    
            self.dungeon.place_rooms()
            self.dungeon.connect_rooms()
            self.grid = self.dungeon.grid
        print('Generating characters...')
        self.character_count = 0
        self.add_character(self.create_random_character())
        self.player = self.characters[0]
        self.enemy = create_enemy(random.randint(0, 4), self.grid)
        print('Adding catalogues...')
        self.grid.goods = Goods
        self.grid.armory = Armory
        print('Adding items...')
        self.item_factory = GridItemMetaFactory
        self.item_factory.init_grid(self.grid)
        self.add_random_items(10)
        self.task_list = _task_list
        self.prepare_player()
        print('Done!')
        
    @property
    def items_on_grid(self) -> list:
        class GridItems(dict):
            def __init__(self):
                dict.__init__(self)
                
            def __getitem__(self, key):
                key = key.replace(' ', '').lower()
                return dict.__getitem__(self, key)
            
            def __setitem__(self, key, value):
                key = key.replace(' ', '').lower()
                return dict.__setitem__(self, key, value)
            
            def __ior__(self, other):
                for key in other:
                    self[key.lower().replace(' ', '')] = other[key]
                return self
                            
        grid_items = GridItems() 
        goods = self.grid.goods._grid_instances
        armory = self.grid.armory._grid_instances
        grid_items |= armory
        grid_items |= goods
        
        return grid_items
    
    @property
    def item_list(self) -> list:
        return list(self.grid.goods.general_manifest)+list(self.grid.goods.trade_manifest)+list(self.grid.armory.weapons_manifest)+list(self.grid.armory.armor_manifest)
    
    def pickup_item(self, item: Any, character: Any) -> None:
        character.pickup(item)
        item.cell.entry_object['items'] = {}
        item.cell = None
    
    def add_character(self, character) -> None:
        self.character_count += 1
        self.characters.append(character)
        
    def create_random_character(self):
        create(grid=self.grid)
        return getattr(character_bank, f'char{self.character_count+1}')
    
    def add_item(self, item_name: str = None, cell: Union[str, object] = None) -> None:
        if item_name is None and cell is None:
            GridItemMetaFactory.create_random_item()
        elif item_name is not None and cell is None:
            GridItemMetaFactory.create_item_by_class(item_name)
        elif item_name is None:
            GridItemMetaFactory.create_random_item(cell=cell)
        else:
            GridItemMetaFactory.create_item(item_name, cell)
            
        
    def add_random_item(self, cell = None):
        self.add_item(cell=cell)
        
    def add_random_items(self, n: int):
        for _ in range(n):
            self.add_random_item()

    def give_player_item(self, item_name: str):
        self.player.inventory.add_item(item_name)
        
    def prepare_player(self):
        for _ in range(10):
            self.player.inventory.add_item('OakLog')
            self.player.inventory.add_item('IronOre')
        self.player.inventory.add_item('Tongs')
        self.player.inventory.add_item('Axe')
        
    def process_enemy_actions(self):
        return process_enemy_actions(self.grid, self.enemy, player=self.player) 
