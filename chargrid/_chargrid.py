import random
from typing import Union
from CharActor import create, character_bank, Catalogues
from grid_engine import Grid
from .meta import *

# Let's create a class to hold our game state
# The game state will include the grid and the characters
# We'll also attach the Catalogues, `Goods` and `Armory` to the grid object
# so that the characters can access them easily. 
class Game:
    _grid = None
    _characters = None
    
    @property
    def grid(self) -> type(Grid.Grid):
        return self._grid
    
    @grid.setter
    def grid(self, grid: type(Grid.Grid)) -> None:
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
        
    def __init__(self):
        print('Generating grid...')
        self.grid = Grid.Grid(cell_size=1, dimensions=(300, 300))
        print('Generating characters...')
        self.character_count = 0
        self.add_character(self.create_random_character())
        print('Adding catalogues...')
        self.grid.catalogues = Catalogues
        self.grid.goods = Catalogues.Goods
        self.grid.armory = Catalogues.Armory
        print('Adding items...')
        self.item_factory = GridItemMetaFactory
        self.item_factory.init_grid(self.grid)
        self.add_random_items(10)
        print('Done!')
        
    @property
    def items_on_grid(self) -> list:
        grid_items = {}
        goods = self.grid.goods._grid_instances
        armory = self.grid.armory._grid_instances
        grid_items |= armory
        grid_items |= goods
        return grid_items
    
    @property
    def item_list(self) -> list:
        return list(self.grid.goods.general_manifest)+list(self.grid.goods.trade_manifest)+list(self.grid.armory.weapons_manifest)+list(self.grid.armory.armor_manifest)
        
    def add_character(self, character) -> None:
        self.character_count += 1
        self.characters.append(character)
        character._join_grid(self.grid)
        
    def create_random_character(self):
        create()
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