from chargrid import Game, Grid, Item, ItemStack
import grid_engine as ge
import curses
from colorama import Fore
from subprocess import call
import time
from time import sleep
import numpy as np
import os, sys
import re

def clear():return call('clear')
def tick():sleep(0.1),clear()
def long_tick():sleep(1),clear()
def stop():sleep(3), clear()

r = Fore.RESET
red = Fore.LIGHTRED_EX
green = Fore.LIGHTGREEN_EX
blue = Fore.LIGHTBLUE_EX
yellow = Fore.LIGHTYELLOW_EX
magenta = Fore.LIGHTMAGENTA_EX
cyan = Fore.LIGHTCYAN_EX
white = Fore.LIGHTWHITE_EX

# sys.ps1 = f'{blue}>>> {white}'

# tick()

# print(f'{white}Preparing {blue}demo{white}...')
# stop()

# print(f'Creating {blue}game{white}...')
# stop()


# print(f'Call {blue}game{white} using `{green}game{white}` ...')
# stop()

# print(f'Identifying {blue}character{white}...')
# stop()

# print(f'Call {blue}character{white} using `{green}char{white}` ...')
# stop()

# print(f'Identifying {blue}grid{white} ...')
# stop()


# print(f'Call {blue}grid{white} using `{green}grid{white}` ...')
# stop()

# tick()

# print('All done.')
# stop()

def determine_sections(grid, char_x, char_y, max_x, max_y):
    # Determine the sections of the grid that should be drawn based on the character's initial position
    # The sections will follow a (x, y) coordinate system with the origin at the top left corner of the grid
    # The sections will be returned as a np.array of tuples
    # Each tuple will contain the top left coordinates and bottom right coordinates of the section
    # The sections will be drawn as needed based on the character's movement
    # initialize the array
    sections = np.array([((0, 0), (max_x-2, max_y-2))])
    # determine the number of sections needed
    # the number of sections will be determined by the size of the grid and the size of the terminal
    section_count_x = grid.blueprint.col_count // (max_x - 2)
    section_count_y = grid.blueprint.row_count // (max_y - 2)
    first_screen_index = 0
    if section_count_x == 1 and section_count_y == 1:   
        return sections, first_screen_index
    else:
        for y in range(section_count_y):
            for x in range(section_count_x):
                if x == 0 and y == 0:
                    continue
                x1, y1 = (x * (max_x-2), y * (max_y - 2))
                x2, y2 = (x1 + (max_x-2), y1 + (max_y - 2))
                sections = np.append(sections, [((x1, y1), (x2, y2))], axis=0)
                if char_x in range(x1, x2) and char_y in range(y1, y2):
                    first_screen_index = len(sections) - 1
        return sections, first_screen_index

# Draw functions

def draw_screen(stdscr, grid, section, enemy):
    max_y, max_x = stdscr.getmaxyx()
    section_tl, section_br = section[0], section[1]

    # draw screen
    for y in range(section_tl[1], section_br[1]):
        for x in range(section_tl[0], section_br[0]):
            win_x, win_y = (min((x - section_tl[0]), max_x - 2), min((y - section_tl[1]), max_y - 2))
            cell_x, cell_y = x, y

            cell = grid[(x, y)]
            items_in_cell = cell.entry_object['items']
            structures_in_cell = cell.entry_object['structures']
            entry_zone = cell.entry_zone

            if grid.with_terrain:
                terrain_str = cell.terrain_str
                terrain_char = cell.terrain_char
                draw_terrain(stdscr, win_x, win_y, terrain_str, terrain_char)
            if entry_zone['areas'] is not None:
                draw_structure(stdscr, win_x, win_y, entry_zone, structures_in_cell)
            if cell.passable:
                stdscr.addstr(win_y, win_x, ' ')
            else:
                stdscr.addstr(win_y, win_x, ' ', curses.color_pair(4))
            draw_item(stdscr, win_x, win_y, items_in_cell)
            draw_occupied_cells(stdscr, grid, cell_y, cell_x, win_x, win_y, enemy)

def draw_terrain(stdscr, win_x, win_y, terrain_str, terrain_char):
    if terrain_str == 'OCEAN':
        stdscr.addstr(win_y, win_x, '~', curses.color_pair(1))
    elif terrain_char == ' ':
        stdscr.addstr(win_y, win_x, ' ', curses.color_pair(0))
    elif terrain_str in ['SAND', 'SEASHELL']:
        stdscr.addstr(win_y, win_x, ' ', curses.color_pair(0))
    elif terrain_char == '^':
        stdscr.addstr(win_y, win_x, '^', curses.color_pair(2))

def draw_item(stdscr, win_x, win_y, items_in_cell):
    if items_in_cell is not None:
        if len(list(items_in_cell.keys())) > 0:
            item_key = list(items_in_cell.keys())[0]
            item = items_in_cell[item_key]
            stdscr.addstr(win_y, win_x, item.name[0].lower())

def draw_structure(stdscr, win_x, win_y, entry_zone, structs):
    if len(list(entry_zone['areas'].keys())) > 0:
        area_key = list(entry_zone['areas'].keys())[0]
        if area_key.startswith('room'):
            if structs is not None:
                if len(list(structs.keys())) > 0:
                    structure_keys = list(structs.keys())
                    for structure_key in structure_keys:
                        if structure_key == 'room':
                            stdscr.addstr(win_y, win_x, ' ', curses.color_pair(0))
                        elif structure_key == 'wooden_wall':
                            stdscr.addstr(win_y, win_x, '#', curses.color_pair(0))
                        elif structure_key == 'door':
                            stdscr.addstr(win_y, win_x, '_', curses.color_pair(0))            

def draw_action_menu(action_menu_win, selection):
    action_menu_win.clear()
    action_menu_win.box()
    action_menu_win.addstr(1, 2, 'Actions')
    action_menu_win.addstr(2, 2, f'1. View Inventory{'<' if selection == 1 else ''}')
    action_menu_win.addstr(3, 2, f'2. View Stats{'<' if selection == 2 else ''}')
    action_menu_win.addstr(4, 2, f'3. View Map{'<' if selection == 3 else ''}')
    action_menu_win.addstr(5, 2, f'4. Setup Camp{'<' if selection == 4 else ''}')
    action_menu_win.addstr(6, 2, f'5. View key bindings{'<' if selection == 5 else ''}')
    action_menu_win.addstr(7, 2, f'6. Settings{'<' if selection == 6 else ''}')
    action_menu_win.addstr(8, 2, f'7. Save Game{'<' if selection == 7 else ''}')
    action_menu_win.addstr(9, 2, f'8. Quit{'<' if selection == 8 else ''}')
    action_menu_win.refresh()
    
def draw_stats(sub_menu_win, character):
    sub_menu_win.clear()
    sub_menu_win.box()
    sub_menu_win.addstr(1, 2, f'{character.name} Level {character.level} {character._alignment.title} {character._race.title} {character._role.title}')
    sub_menu_win.addstr(3, 2, f'HP: {character.hp}')
    sub_menu_win.addstr(3, 6, f'AC: {character.armor_class}')
    sub_menu_win.addstr(5, 2, f'{character.Strength}')
    sub_menu_win.addstr(6, 2, f'{character.Dexterity}')
    sub_menu_win.addstr(7, 2, f'{character.Constitution}')
    sub_menu_win.addstr(5, 16, f'{character.Intelligence}')
    sub_menu_win.addstr(6, 16, f'{character.Wisdom}')
    sub_menu_win.addstr(7, 16, f'{character.Charisma}')
    sub_menu_win.addstr(9, 2, f'     Saving Throws')
    sub_menu_win.addstr(10, 2, f'Fort       Ref       Will')
    sub_menu_win.addstr(11, 2, f' {character.saving_throws["Fortitude"]}          {character.saving_throws["Reflex"]}          {character.saving_throws["Will"]}')
    weapon = character.inventory.equipment['MAIN_HAND']
    if weapon is not None:
        sub_menu_win.addstr(13, 2, f'Weapon: {character.inventory.equipment['MAIN_HAND'].name}')
        sub_menu_win.addstr(13, 25, 'Damage        Damage Type       Range')
        sub_menu_win.addstr(14, 2, f'Atk Bonus: +{character.Strength.modifier}')
        sub_menu_win.addstr(14, 26, f'{character.inventory.equipment["MAIN_HAND"].damage[0]}d{character.inventory.equipment['MAIN_HAND'].damage[1].value}          {character.inventory.equipment['MAIN_HAND'].damage_type}      {character.inventory.equipment["MAIN_HAND"].weapon_range}')
    else:
        sub_menu_win.addstr(13, 2, 'Unarmed')

    sub_menu_win.addstr(1, 128, 'Skills')
    for i, skill in enumerate(character.skillbook.items.keys()):
        sub_menu_win.addstr(3 + i, 128, f'{skill.replace('_', ' ')}: {character.skillbook.values()[i]}')
    sub_menu_win.refresh()

def draw_sub_menu(sub_menu_win, selected_menu, character):
    sub_menu_win.addstr(0, ((sub_menu_win.getmaxyx()[1]//2) - len(selected_menu)//2), selected_menu)
    sub_menu_win.refresh()
    
def draw_inventory(sub_menu_win, character, selected_item=1):
    max_y, max_x = sub_menu_win.getmaxyx()
    for i, item in enumerate(character.inventory, start=1):
        item = re.sub(r'(?<!\s)([A-Z])', r' \1', item)
        if i < max_y:
            sub_menu_win.addstr(i, 2, f'{'>' if selected_item == i else ''}{item}     ')    
        else:
            sub_menu_win.addstr((i) - (max_y - 2), 30 , f'{'>' if selected_item == i else ''}{item}     ')
    sub_menu_win.refresh()
    
def draw_enemy_name(stdscr, enemy):
    max_y, max_x = stdscr.getmaxyx()
    stdscr.addstr(max_y - 3, max_x - 30, f'{enemy.monster_name}')
    
def draw_time(time_win, step_count):
    time_win.clear()
    time_win.box()
    time_win.addstr(1, 2, f'Time: {get_time(step_count)}')
    time_win.refresh()
    
def draw_occupied_cells(stdscr, grid, y, x, win_x, win_y, enemy):
    cell = grid[(x, y)]
    enemy_cell = enemy.cell
    y, x = win_y, win_x

    is_cell_occupied = cell.occupied
    is_screen_occupied = stdscr.inch(y, x) == ord('@')
    
    is_enemy_dead = enemy.hp <= 0

    if is_cell_occupied and not is_screen_occupied:
        stdscr.addstr(y, x, '@')
    elif not is_cell_occupied and is_screen_occupied:
        stdscr.addstr(y, x, ' ')
        
    if cell == enemy_cell and is_enemy_dead:
        stdscr.addstr(y, x, '%')

# Echo functions

def echo_mvmnt(mvmnt_box, mvmnt):
    if mvmnt is not None:
        mvmnt_box.box()
        mvmnt_box.clear()
        mvmnt_box.addstr(1, 2, f'{mvmnt}')
        mvmnt_box.refresh()
        
def echo_pickup(pickup_box, item_name):
    if item_name is not None:
        pickup_box.box()
        pickup_box.clear()
        pickup_box.addstr(1, 2, f'Picked up{item_name}')
        pickup_box.refresh()
        
def echo_damage(damage_win, attack):
    if attack is not None:
        damage_win.box()
        damage_win.clear()
        damage_win.addstr(1, 2, f'{attack}')
        damage_win.refresh()
        
def echo_attack(attack_win, attack):
    if attack is not None:
        attack_win.box()
        attack_win.clear()
        attack_win.addstr(1, 2, f'{attack}         ')
        attack_win.refresh()

def echo_results(mvmnt, atk, previous_atk, item_name, enemy_action, damage_win, atk_win, mvmnt_box, pickup_box, time_win, game_over_win, step_count):
    if mvmnt is not None:
        echo_mvmnt(mvmnt_box, mvmnt)
    if atk is not None:
        echo_attack(atk_win, atk)
    else:
        echo_attack(atk_win, previous_atk)    
    if item_name is not None:
        echo_pickup(pickup_box, item_name)    
    if enemy_action is not None and enemy_action not in ['move', 'wait']:
        echo_damage(damage_win, enemy_action)
    draw_time(time_win, step_count)

# Input processing functions
   
def process_input(key, stdscr, character, section, grid, action_menu_win, sub_menu_win, build_win):
    if key == 'x':
        action_menu(key, stdscr, action_menu_win, sub_menu_win, character, grid)
        result = (None, None)
    elif key in '123456789':
        result = process_movement_input(key, character)
    elif key == 'a':
        result = process_attack_input(key, stdscr, character, section, grid)
    elif key == 'z':
        result = process_pickup_input(key, character, grid)
        if result is None:
            result = (None, None)
    elif key == 'b':
        process_build_input(key, stdscr, build_win, character, section, grid)
        result = (None, None)
    else:
        result = (None, None)
    return result

def process_movement_input(key, char):
    mvmnt = None
    if key == '1':
        mvmnt = char.move('south_west')
    elif key == '2':
        mvmnt = char.move('south')
    elif key == '3':
        mvmnt = char.move('south_east')
    elif key == '4':
        mvmnt = char.move('west')
    elif key == '5':
        char.end_turn()
    elif key == '6':
        mvmnt = char.move('east')
    elif key == '9':
        mvmnt = char.move('north_east')
    elif key == '8':
        mvmnt = char.move('north')
    elif key == '7':
        mvmnt = char.move('north_west')
    return ('mvmnt', mvmnt)

def process_attack_input(key, stdscr, character, section, grid):
    return ('atk', player_attack(stdscr, character, section, grid))

def process_pickup_input(key, character, grid):
    for cell in character.cell.adjacent:
        if cell is not None:
            if grid[cell].entry_object['items'] is not None:
                if len(list(grid[cell].entry_object['items'].keys())) > 0:
                    item_key = list(grid[cell].entry_object['items'].keys())[0]
                    item = grid[cell].entry_object['items'][item_key]
                    item_name = item.name
                    character.inventory.pick_up(item)
                    grid[cell].entry_object['items'] = {}
                    return ('item_name', re.sub(r'(?<!\s)([A-Z])', r' \1', item_name))
    return None

def process_build_input(key, stdscr, build_win, character, section, grid):
    if key == 'b':
        build_object = None
        build_cell = None
        selected_cell = None
        selection = 1
        char_cell = character.cell
        relative_index = 0
        while build_object is None:
            build_win.clear()
            build_win.box()
            build_win.addstr(1, 2, 'Build')
            build_win.addstr(2, 2, f'1. Wooden Wall{"<" if selection == 1 else ""}')
            build_win.addstr(3, 2, f'2. Wooden Door{"<" if selection == 2 else ""}')
            build_win.refresh()
            key = stdscr.getkey()
            if key == "KEY_DOWN":
                selection += 1
                if selection > 2:
                    selection = 1
            elif key == "KEY_UP":
                selection -= 1
                if selection < 1:
                    selection = 2
            elif key == "b":
                if selection == 1:
                    build_object = 'wooden_wall'
                elif selection == 2:
                    build_object = 'door'
                break
        build_win.clear()
        build_cell = choose_cell(stdscr, grid, character, section, 'b')
        if build_object == 'wooden_wall':
            ge.grid_object.build_wall(grid, build_cell)
        elif build_object == 'door':
            ge.grid_object.build_door(grid, build_cell)
        curses.curs_set(0)
        return
        
def player_attack(stdscr, character, section, grid):
    attack_cell = choose_cell(stdscr, grid, character, section, 'a')
    if attack_cell.occupant is not None:
        character.target = attack_cell.occupant.parent
        if character.target is not None:
            return character.attack()
    return None

def action_menu(key, stdscr, action_menu_win, sub_menu_win, character, grid):
        sub = interact_action(stdscr, action_menu_win)
        sub_menu = get_sub_menu(sub_menu_win, sub)
        draw_sub_menu(sub_menu_win, sub_menu, character)
        if sub_menu == 'Inventory':
            interact_inventory(stdscr, sub_menu_win, character)
        elif sub_menu == 'Stats':
            draw_stats(sub_menu_win, character)
            key = stdscr.getkey()

def get_relative_coordinates(stdscr, section, target_cell):
    max_y, max_x = stdscr.getmaxyx()
    section_tl, section_br = section[0], section[1]
    cell_x, cell_y = target_cell.coordinates
    
    return (min(1 + (cell_x - section_tl[0]), max_x - 2), min(1 + (cell_y - section_tl[1]), max_y - 2))    
    
def interact_inventory(stdscr, sub_menu_win, character):
    selected_item = 1
    inspect = False
    leave = False
    while not inspect and not leave:
        draw_inventory(sub_menu_win, character, selected_item)
        key = stdscr.getkey()
        if key == 'KEY_DOWN':
            selected_item += 1
            if selected_item > len(character.inventory.items):
                selected_item = 1
        elif key == 'KEY_UP':
            selected_item -= 1
            if selected_item < 1:
                selected_item = len(character.inventory.items)
        elif key == 'i':
            inspect = True
        elif key == 'x':
            leave = True
    if inspect:
        sub_menu_win.clear()
        sub_menu_win.box()
        if isinstance(character.inventory.items[selected_item - 1], ItemStack):
            pass
        sub_menu_win.addstr(2, 2, character.inventory.items[selected_item - 1].description)
        sub_menu_win.refresh()
        stdscr.getkey()
    elif leave:
        sub_menu_win.clear()
        sub_menu_win.refresh()
        
def interact_action(stdscr, action_menu_win):
    selection = 1
    sub = None
    while sub == None:
        draw_action_menu(action_menu_win, selection)
        key = stdscr.getkey()
        if key == 'KEY_DOWN':
            selection += 1
            if selection > 8:
                selection = 1
        elif key == 'KEY_UP':
            selection -= 1
            if selection < 1:
                selection = 8
        elif key == 'x':
            sub = selection
            selection = None
    return sub
                    
def choose_cell(stdscr, grid, character, section, confirmation_key):
        char_cell = character.cell
        chosen_cell = None
        selected_cell = grid[char_cell.adjacent[0]]
        y, x = stdscr.getyx()
        curses.curs_set(1)
        relative_index = 0
        while chosen_cell is None:
            selected_cell = grid[char_cell.adjacent[relative_index]]
            relative_coords = get_relative_coordinates(stdscr, section, selected_cell)
            stdscr.move(relative_coords[1]-1, relative_coords[0]-1)
            key = stdscr.getkey()
            if key == "KEY_DOWN":
                if relative_index == 0:
                    relative_index = 7
                elif relative_index in [2, 3]:
                    relative_index += 1
                elif relative_index == 7:
                    relative_index = 6
                elif relative_index == 1:
                    relative_index = 5                
            elif key == "KEY_UP":
                if relative_index == 7:
                    relative_index = 0
                elif relative_index in [3, 4]:
                    relative_index -= 1
                elif relative_index == 6:
                    relative_index = 7
                elif relative_index == 5:
                    relative_index = 1
            elif key == "KEY_LEFT":
                if relative_index in [1, 2]:
                    relative_index -= 1
                elif relative_index in [4, 5]:
                    relative_index += 1
                elif relative_index == 3:
                    relative_index = 7
            elif key == "KEY_RIGHT":
                if relative_index in [0, 1]:
                    relative_index += 1
                elif relative_index in [5, 6]:
                    relative_index -= 1
                elif relative_index == 7:
                    relative_index = 3
            if key == confirmation_key:
                chosen_cell = selected_cell
                break
        stdscr.move(y, x)
        curses.curs_set(0)
        return chosen_cell
                    
def get_sub_menu(sub_menu_win, selection):
    sub_menu_win.clear()
    sub_menu_win.box()
    sub_menus = [
        'Inventory',
        'Stats',
        'Map',
        'Camp',
        'Key Bindings',
        'Settings',
        'Save Game',
        'Quit'
]
    return sub_menus[selection - 1]

def get_time(step_count):
    seconds = (step_count * 10) % 60
    minutes = ((step_count * 10) // 60) % 60
    hours = (((step_count * 10) // 60) // 60) % 24
    days = ((((step_count * 10) // 60) // 60) // 24)
    return f'{days}d {hours}h {minutes}m {seconds}s'
    
def main(stdscr): # type: curses._CursesWindow
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_color(curses.COLOR_GREEN, 74, 255, 128)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_color(curses.COLOR_YELLOW, 255, 130, 145)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_color(8, 133, 133, 133)
    curses.init_pair(4, 8, 8)

    stdscr.keypad(True)    
    
    max_y, max_x = stdscr.getmaxyx()        
    print(f'Terminal size: Rows = {max_y}, Columns = {max_x}')

    grid = None
    mvmnt_box = curses.newwin(3, 22, max_y - 5, max_x - 55)
    pickup_box = curses.newwin(3, 30, max_y - 10, max_x - 55)
    action_menu_win = curses.newwin(12, 30, max_y // 4, max_x // 4)
    sub_menu_win = curses.newwin(max_y - 10, max_x - 20, 5, 10)
    time_win = curses.newwin(3, 30, 3, 3)
    build_win = curses.newwin(12, 30, max_y // 4, max_x // 4)
    damage_win = curses.newwin(3, 30, max_y - 15, max_x - 55)
    game_over_win = curses.newwin(max_y // 3, max_x // 3, max_y // 3, max_x // 3)
    atk_win = curses.newwin(3, 30, max_y - 20, max_x - 55)
    step_count = 0
    game_time = 0
    
        
    while grid is None:
        sys.stdout = open(os.devnull, 'w')
        # big grid
        # dimensions = (max_x - 2) * 5, (max_y - 2) * 5
        # small grid
        dimensions = max_x - 2, max_y - 2
        
        game = Game(map_type='dungeon', dimensions=dimensions)

        grid: Grid.Grid = game.grid
    
    sys.stdout = sys.__stdout__

    char = game.player
    
    monster = game.enemy
    
    char_x, char_y = char.cell.coordinates
    
    sections, first_screen_index = determine_sections(grid, char_x, char_y, max_x, max_y)
    
    current_section = sections[first_screen_index]
    
    draw_screen(stdscr, grid, current_section, monster)
    
    mvmnt = None
    atk = None
    previous_atk = None
    selection = None
    item_name = None
    enemy_action = None
    previous_enemy_action = None
    result = (None, None)
        
    while True:
        for i, section in enumerate(sections):
            if char_x in range(section[0][0], section[1][0]) and char_y in range(section[0][1], section[1][1]):
                current_section = section
        char_x, char_y = char.cell.coordinates
        
        key = stdscr.getkey()
        if key == 'q':
            break
        else:
            result = process_input(key, stdscr, char, current_section, grid, action_menu_win, sub_menu_win, build_win)
        
        if result[0] == 'mvmnt':
            mvmnt = result[1]
        if result[0] == 'atk':
            atk = result[1]
            previous_atk = atk
        else:
            previous_atk = atk
            atk = None
        if result[0] == 'item_name':
            item_name = result[1]
        
        if any([mvmnt, atk]):
            step_count += 1

        if game.enemy.hp > 0:
            enemy_action = game.process_enemy_actions()
        else:
            enemy_action = None
        previous_enemy_action = enemy_action if enemy_action is not None and enemy_action not in ['move', 'wait'] else previous_enemy_action

        draw_screen(stdscr, grid, current_section, monster)
        stdscr.refresh()
        echo_results(mvmnt, atk, previous_atk, item_name, enemy_action, damage_win, atk_win, mvmnt_box, pickup_box, time_win, game_over_win, step_count)
        # echo_mvmnt(mvmnt_box, mvmnt)
        # echo_pickup(pickup_box, item_name)
        # echo_damage(damage_win, enemy_action)
        # echo_attack(atk_win, previous_atk)    
        # draw_time(time_win, step_count)
        draw_enemy_name(stdscr, game.enemy)
        if char.hp <= 0:
            game_over_win.box()
            game_over_win.addstr((max_y // 3) // 2, ((max_x // 3) // 2) - 4, 'Game Over')
            game_over_win.refresh()
            stdscr.getkey()
            break


curses.wrapper(main)