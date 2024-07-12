
# chargrid
Is a flirtatious implementation of my other programs [dicepy](https://github.com/primal-coder/dicepy), [entyty](https://github.com/primal-coder/entyty), [CharActor](https://github.com/primal-coder/charactor) [CharMonster](http://github.com/primal-coder/charmonster) and [grid-engine](https://github.com/primal-coder/grid-engine). Install the package with `pip install chargrid` and you can get a quick demo with `python -m chargrid`. Everything is basically a work in progress. The main idea is to have the means to create a textual, grid-based role-playing game/engine. At this point, you may draw comparisons to HackNet, which are not far off, in fact you might say it's a HackNet clone. The player is represented by an '@' symbol, you can use the numpad to navigate the generated layout, items are represented by the first letter in the item's name, enemies are represented by '@' signs(which will be changed in the future), you can construct walls which will be represented on the grid and will impeded movement, you can attack in squares surrounding you, etc.

## Controls

- Movement: Numpad 1, 2, 3, 4, 6, 7, 8, 9
- Attack: 'A' to initiate attack-mode, the arrow keys to navigate the cursor and 'A' to confirm which cell to direct the attack
- Build: 'B' to display the build menu, 'B' to confirm the build piece, the arrow keys to navigate the cursor and 'B' to confirm the cell in which the piece will be built.
- Pickup: 'Z' when positioned adjacent to a cell containing an item, if positioned near multiple items all items will be picked up.
- Menu: 'X' to display the menu, 'X' to confirm the selection and 'X' to close the menu.

There is still a long way to go to having the openworld, gridcentric, text-based, sandbox rpg I have in mind(think Skyrim meets Hacknet meets ... goosebumps?). But I'm working on it. 
