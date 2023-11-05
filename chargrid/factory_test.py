from chargrid.meta import *
import CharActor as ca
import grid_engine as ge

# Let's define a function to load some items onto the grid.
def load_grid_items(grid):
    for _ in range(10):
        GridItemMetaFactory.create_random_item(grid)

# Let's declare our grid and attach the Catalogues, `Goods` and `Armory` to it.
grid = ge.Grid.Grid(cell_size=5, dimensions=(1920, 1080), noise_scale=511, noise_octaves=83, noise_roughness=0.3)
setattr(grid, 'goods', Goods)
setattr(grid, 'armory', Armory)

# 
# Let's render the grid and see what it looks like.
dimensions = grid.blueprint.grid_dimensions
cdata = ge._grid.extract_cell_data(grid)
cell_size = grid.cell_size
grid_id = grid.grid_id

del grid

ge._utility.generate_images(dimensions, cdata, cell_size, grid_id, True)

