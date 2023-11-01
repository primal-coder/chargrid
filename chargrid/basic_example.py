from grid_engine import Grid
from CharActor import create, character_bank

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
        
    def add_character(self, character) -> None:
        self.character_count += 1
        self.characters.append(character)
        character._join_grid(self.grid)
        
    def create_random_character(self):
        create()
        return getattr(character_bank, f'char{self.character_count+1}')
    