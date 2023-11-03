import re
import random
import CharActor as CA
from grid_engine._grid_object.grid_item import GridItem

Goods = CA.Catalogues.Goods
Armory = CA.Catalogues.Armory
classes = list(Goods.items.values()) + list(Armory.items.values())

class GridItemMetaFactory:
    @staticmethod
    def create_item_by_class(grid, cell, Class):
        instance = type(Class.__name__, (GridItem, Class), {})(grid=grid, cell=cell, name=Class.__name__)
        if instance.name in Goods.items.keys():
            Goods._grid_instances[instance.name] = instance
        elif instance.name in Armory.items.keys():
            Armory._grid_instances[instance.name] = instance
        return instance
    
    @staticmethod
    def create_random_item(grid, cell = None):
        Class = random.choice(classes)
        if cell is None:
            cell = grid.random_cell(attr=('passable', True))
        return GridItemMetaFactory.create_item_by_class(grid, cell, Class)
    
    @staticmethod
    def create_item(item_name, grid, cell = None):
        item_name = re.sub(r'([a-z])([A-Z])',r'\1 \2', item_name.title().replace(' ', '', len(item_name.split()) - 1))
        class_names = [cls.__name__ for cls in classes]
        if item_name in class_names:
            Class = classes[class_names.index(item_name)]
            if cell is None:
                cell = grid.random_cell(attr=('passable', True))
            return GridItemMetaFactory.create_item_by_class(grid, cell, Class)
            