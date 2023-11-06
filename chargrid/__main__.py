from chargrid import Game, Grid, Catalogues

game = Game()

char = game.characters[0]

grid: Grid.Grid = game.grid

perimeter = grid.get_perimeter(grid.get_area(char.cell, 3))
for cell in perimeter:
    game.add_item(cell=cell)