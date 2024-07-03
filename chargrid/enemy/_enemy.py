from typing import Union
import CharActor as ca
import CharMonster as cm
import entyty
from random import choice
import re

def all_equal(iterable):
    return all(x == iterable[0] for x in iterable)

def create_enemy(enemy_number, grid):
    return cm.Monster(enemy_number, grid=grid)
    # ca.create(obj_name, enemy_name, role='Fighter', race='Human', alignment='chaotic_evil', background='Soldier', grid = grid)
    # return getattr(ca.character_bank, obj_name)

def check_line_of_sight(grid, enemy: Union[entyty.GridEntity, ], player: Union[entyty.GridEntity, ]):
    enemy_cell = enemy.cell.designation
    player_cell = player.cell.designation
    enemy_vision = enemy.vision // 10
    if grid.get_distance(enemy_cell, player_cell) <= enemy_vision:
        path, cost = grid.get_path(enemy_cell, player_cell)
        directions = []
        for i, cell in enumerate(path):
            cell = grid[cell]
            next_cell = grid[path[i + 1]] if i + 1 < len(path) else None
            if next_cell is None:
                break
            direction = grid.get_direction(cell, next_cell)
            directions.append(direction)
        if all_equal(directions):
            return True
    return False

def process_enemy_actions(grid, enemy: Union[entyty.GridEntity, ], player: Union[entyty.GridEntity, ]):
    if enemy.hp <= 0:
        return 'dead'
    enemy_cell = enemy.cell.designation
    player_cell = player.cell.designation
    enemy_vision = 20
    if grid.get_distance(enemy_cell, player_cell) <= enemy_vision:
        if grid.get_distance(enemy_cell, player_cell) == 1:
            enemy.set_target(player)
            attack_result = enemy._attack_figure()
            return attack_result
        # if check_line_of_sight(grid, enemy, player):
        path, cost = grid.get_path(enemy_cell, player_cell)
        if len(path) > 1:
            enemy.move(cell=path[0])
            return 'move'
    action = choice(['move', 'wait', 'wait'])
    if action == 'move':
        direction = choice(['north', 'south', 'east', 'west'])
        enemy.move(direction=direction)
        return 'move'
    else:
        return 'wait'
