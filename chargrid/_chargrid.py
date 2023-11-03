import random
from typing import Union
from CharActor import create, character_bank, Catalogues
from grid_engine import Grid, Cell, Blueprint

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
        self.grid = Grid.Grid(cell_size=1, dimensions=(500, 500))
        self.character_count = 0
        self.add_character(self.create_random_character())
        self.grid.catalogues = Catalogues
        self.grid.goods = Catalogues.Goods
        self.grid.armory = Catalogues.Armory
        
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
        return list(self.grid.goods.items.keys())+list(self.grid.armory.items.keys())
        
    def add_character(self, character) -> None:
        self.character_count += 1
        self.characters.append(character)
        character._join_grid(self.grid)
        
    def create_random_character(self):
        create()
        return getattr(character_bank, f'char{self.character_count+1}')
    
    def add_item(self, item_name: str, cell: Union[str, object] = None) -> None:
        if cell is None:
            cell = self.grid.random_cell(attr=('passable', True))
        if isinstance(cell, str):
            cell = self.grid[cell]
        if item_name is None:
            item_name = random.choice(list(self.grid.goods.items.keys())+list(self.grid.armory.items.keys()))
        self.grid.catalogues.get(item_name, self.grid, cell)

    def add_random_item(self):
        self.add_item(None)
        
    def add_random_items(self, n: int):
        for _ in range(n):
            self.add_random_item()