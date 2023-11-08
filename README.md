# chargrid
Is a flirtatious implementation of my other programs [dicepy](https://github.com/primal-coder/dicepy), [entyty](https://github.com/primal-coder/entyty), [CharActor](https://github.com/primal-coder/charactor) and [grid-engine](https://github.com/primal-coder/grid-engine). Install the package with `pip install chargrid` and you can get a quick demo with `python -im chargrid`. Everything is basically a work in progress, after the initial setup you can perform a number of actions using objects from each of the modules. 

type
```python
>>> char      
Unnamed, Half-Orc Sorcerer
>>> char.
```

The main idea is to have a simple way to create a grid based game with a text interface. At this point, a character can be created(using CharActor/entyty) and placed on the grid(grid-engine/entyty). The character is complete with attributes much like a traditional rpg. The character can be moved around the grid. There is a limitation to how much you can move in a single turn(right now called move_energy). Once its gone you would have to end your turn and await the round of turns to complete, but for now there's no enemies as I haven't worked out the Turn Manager yet. So calling `char.end_turn()` will simply refill your move_energy. But you can also call `char.look_around()` to return whether the character has any items of interest within sight. Ultimately the same methodology will be used to provide an in-depth text description of a character's surroundings(including terrain, towns, weather, points of interest, enemies, friendly npcs, etc. and the direction in which they are located relative to the player.) 

There is still a long way to go to having the openworld, gridcentric, text-based, sandbox rpg I have in mind(think Skyrim meets Hacknet meets ... goosebumps?). But I'm working on it. 