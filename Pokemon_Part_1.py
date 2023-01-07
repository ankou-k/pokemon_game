from Pokemon_Part_1_Game_File import *
import random

class Tile:
    def __init__(self, pokemons):
        self.wild_pokemons = pokemons

    def spawn_pokemon(self):
      length = len(self.wild_pokemons)
      if length == 0:
        print("Sorry, no pokemon in this area.")
      else:
        return random.choice(self.wild_pokemons)

class Trainer:
    def __init__(self, name):
        self._position = [0, 0] # x- & y-coordinates are initialized to [0, 0]
        self._name = name
        self._pokedex = set()
        self._pokemons = []

    # Getters/Accessors
    def get_name(self):
        return self._name

    def get_pokedex(self):
        return self._pokedex

    def get_pokemons(self):
        return self._pokemons

    def get_position(self):
        return self._position

    def catch_pokemon(self, pokemon):
        clone = type(pokemon)(pokemon.get_name())
        self._pokedex.add(clone.get_name())
        self._pokemons.append(clone)
        clone.change_trainer(self)
        print("You have caught " + clone.get_name())

    def walk(self, direction):
        ###################################################################
        # Changes position of trainer according to direction              #
        #                                                                 #
        # @params direction is a character of either 'w', 'a', 's' or 'd' #
        ###################################################################
      if direction == 'w' and self._position[1] != 0:
        self._position[1] -= 1
      elif direction == 's' and self._position[1] == 0:
        self._position[1] += 1
      elif direction == 'a' and self._position[0] == 1:
        self._position[0] -= 1
      elif direction == 'd' and self._position[0] == 0:
        self._position[0] += 1
      else:
        print("Invalid move!")
      self.show_position()

    def show_position(self):
        position = self._position
        if (position == [0, 0]):
            print("""
__________________________
            |            |
You are     |            |
here!       |            |
____________|____________|
            |            |
            |            |
            |            |
____________|____________|
""")
        elif (position == [0, 1]):
            print("""
__________________________
            |            |
            |            |
            |            |
____________|____________|
            |            |
You are     |            |
here!       |            |
____________|____________|
""")

        elif (position == [1, 0]):
            print("""
__________________________
            |            |
            | You are    |
            | here!      |
____________|____________|
            |            |
            |            |
            |            |
____________|____________|
""")
        else:
            print("""
__________________________
            |            |
            |            |
            |            |
____________|____________|
            |            |
            | You are    |
            | here!      |
____________|____________|
""")

class Pokemon:
    def __init__(self, name):
        ################################################
        # Pokemon has a name and trainer;              #
        # Initialize trainer to None for wild Pokemons #
        ################################################
        self._name = name
        self._trainer = None

    # Getters/Accessors
    def get_name(self):
        return self._name

    def get_trainer(self):
        return self._trainer

    # Modifiers/Mutators
    def change_trainer(self, trainer):
        self._trainer = trainer
