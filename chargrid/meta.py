from typing import Type
import random
from CharObj import Item as _Item
from grid_engine import grid as Grid, cell as Cell, grid_object as GridObject


class GridItemMetaFactory:
    """This class merges the functionality of the Goods and Armory catalogues 
    present in the CharObj module and the GridItem class present in the GridObject submodule of the grid_engine module.
    The purpose of this class is to allow the creation of items that inherit from GridItem and a class of item present 
    in the catalogues. Thereby, the items created will automatically be added to the grid. The items created with this class
    can be interacted with by characters created using the CharActor module, provided the two inhabit the same grid. 
    The class also provides a method to create a random item and a method to create an item by name. The class also 
    provides a method to check that the GRID variable has been set before any items are created.
    
    Attributes:
        GRID (type(Grid.Grid)): The grid to add the items to
        GOODS (type(Goods)): The goods catalogue
        ARMORY (type(Armory)): The armory catalogue
        CLASSES (list): A list of all the classes in the catalogue
    
    Methods:
        init_grid(grid: type(Grid.Grid)): This method sets the variable GRID and CLASSES to the grid and the classes in the catalogues respectively.
        create_item_by_class(Class: type
        create_random_item(cell = None): This method creates an instance of a random class that inherits from GridItem and a class of item present in the catalogues.
        create_item(item_name, cell = None): This method creates an instance of a class that inherits from GridItem and a class of item present in the catalogues.
        _check_grid(): This method checks that the GRID variable has been set before any items are created.
    """
    GRID = None
    GOODS = None
    ARMORY = None
    CLASSES = None

    @staticmethod
    def init_grid(grid: Type[Grid.Grid]):
        """This method sets the variable GRID and CLASSES to the grid and the classes in the catalogues respectively."""
        GridItemMetaFactory.GRID = grid
        GridItemMetaFactory.GOODS = grid.goods
        GridItemMetaFactory.ARMORY = grid.armory
        GridItemMetaFactory.CLASSES = list(grid.goods.items.values()) + list(grid.armory.items.values())
        
    @staticmethod
    def create_item_by_class(Class: Type[_Item], cell: Type[Cell.Cell] = None, no_cell: bool = None) -> Type[GridObject.GridItem]:
        """This method creates an instance of a class that inherits from GridItem and a class of item present in the catalogues.
        It then adds the instance to the appropriate catalogue and returns the instance. By subclassing GridItem, the item will
        automatically be added to the grid.
        
        Args:
            cell (type(Cell.Cell)): The cell to add the item to
            Class (type(_Item)): The class to create an instance of
        
        Returns:
            instance (type(_Item)): The instance of the class created"""
        GridItemMetaFactory._check_grid()
        grid = GridItemMetaFactory.GRID
        Goods = GridItemMetaFactory.GOODS
        Armory = GridItemMetaFactory.ARMORY
        if not no_cell:
            cell = cell if cell is not None else grid.random_cell(attr=('passable', True))
        else:
            cell = None
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

