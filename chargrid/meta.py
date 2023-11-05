import re
import random
import CharActor as CA
from CharActor._objects._items.item import _Item
from grid_engine import Grid, Cell, GridObject
from grid_engine._grid_object.grid_item import GridItem


class GridItemMetaFactory:
    GRID = None
    GOODS = None
    ARMORY = None
    CLASSES = None

    @staticmethod
    def init_grid(grid: type(Grid.Grid)):
        """This method sets the variable GRID and CLASSES to the grid and the classes in the catalogues respectively."""
        GridItemMetaFactory.GRID = grid
        GridItemMetaFactory.GOODS = grid.goods
        GridItemMetaFactory.ARMORY = grid.armory
        GridItemMetaFactory.CLASSES = list(grid.goods.items.values()) + list(grid.armory.items.values())
        
    @staticmethod
    def create_item_by_class(Class: type(_Item), cell: type(Cell.Cell) = None) -> type(GridObject.GridItem):
        """This method creates an instance of a class that inherits from GridItem and a class of item present in the catalogues.
        It then adds the instance to the appropriate catalogue and returns the instance. By subclassing GridItem, the item will
        automatically be added to the grid.
        
        Args:
            grid (type(Grid.Grid)): The grid to add the item to
            cell (type(Cell.Cell)): The cell to add the item to
            Class (type(_Item)): The class to create an instance of
        
        Returns:
            instance (type(_Item)): The instance of the class created"""
        GridItemMetaFactory._check_grid()
        grid = GridItemMetaFactory.GRID
        Goods = GridItemMetaFactory.GOODS
        Armory = GridItemMetaFactory.ARMORY
        cell = cell if cell is not None else grid.random_cell(attr=('passable', True))
        if Class in GridItemMetaFactory.CLASSES:
            grid_class = type(Class.__name__, (GridObject.GridItem, Class), {}) # This creates a new class that inherits from GridItem and the class passed in as an argument
            instance = grid_class(grid=grid, cell=cell, name=Class.__name__) # This creates an instance of the new class and passes in the grid and cell arguments
        grid_instances = {}
        grid_instances |= Goods._grid_instances
        grid_instances |= Armory._grid_instances
        if grid_instances.get(instance.name) is None:
            if instance.name in Goods:
                Goods._grid_instances[instance.name] = instance
            elif instance.name in Armory:
                Armory._grid_instances[instance.name] = instance
        else:
            item_count = sum(bool(item_name.startswith(instance.name))
                         for item_name in grid_instances)
            if instance.name in Goods:
                Goods._grid_instances[f'{instance.name}{item_count+1}'] = instance                                        
            elif instance.name in Armory:
                Armory._grid_instances[f'{instance.name}{item_count+1}'] = instance
        return instance 
    
    @staticmethod
    def create_random_item(cell = None):
        """This method creates an instance of a random class that inherits from GridItem and a class of item present in the catalogues."""
        Class = random.choice(GridItemMetaFactory.CLASSES)
        return GridItemMetaFactory.create_item_by_class(Class, cell)
    
    @staticmethod
    def create_item(item_name, cell = None):
        """This method creates an instance of a class that inherits from GridItem and a class of item present in the catalogues."""
        class_name = item_name.title().replace(' ', '', len(item_name.split()) - 1)
        class_names = [cls.__name__ for cls in GridItemMetaFactory.CLASSES]
        try:
            Class = GridItemMetaFactory.CLASSES[class_names.index(class_name)]
        except ValueError as e:
            raise ValueError(f'{item_name} is not a valid item name.') from e
        return GridItemMetaFactory.create_item_by_class(cell, Class)
    
    @staticmethod
    def _check_grid():
        grid = GridItemMetaFactory.GRID if GridItemMetaFactory.GRID is not None else None
        if grid is None:
            raise ValueError('GridItemMetaFactory.GRID must be set before attempting to create any items. Use GridItemMetaFactory.init_grid(grid) to set the grid.')

