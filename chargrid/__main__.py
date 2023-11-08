from chargrid import Game, Grid, Catalogues
from colorama import Fore
from subprocess import call
from time import sleep

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

tick()
print('Preparing demo...')
stop()

print('Creating game...')
game = Game()
stop()
print('Call game using `game` ...')
stop()

tick()
print('Identifying character...')
stop()

char = game.characters[0]

print('Call character using `char` ...')
stop()

print('Identifying grid ...')
grid: Grid.Grid = game.grid
print('Call grid using `grid` ...')

stop()
perimeter = grid.get_perimeter(grid.get_area(char.cell, 3))

print('Adding random starting items...')
for i in range(len(perimeter)):
    if i % 3 == 0:
        cell = perimeter[i]
        if cell.passable:
            game.add_item(cell=cell)

stop()
print('All done.')
stop()


print('>>> char.look_around()')
char.look_around()