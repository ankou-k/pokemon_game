from Pokemon_Part_2_Game_File import *
import random

class Tile:
    def __init__(self, pokemons):
        self.wild_pokemons = pokemons

    def spawn_pokemon(self):
        length = len(self.wild_pokemons)
        if (length == 0):
            print("No pokemon in this area.")
        else:
            return self.wild_pokemons[random.randint(0, len(self.wild_pokemons) - 1)]

class Trainer:
    def __init__(self, name):
        self.name = name
        self.pokedex = set()
        self.pokemons = []
        self.position = [0, 0]

    def get_name(self):
        return self.name

    def get_pokedex(self):
        return self.pokedex

    def get_pokemons(self):
        return self.pokemons

    def get_position(self):
        return self.position

    def catch_pokemon(self, pokemon):
        clone = type(pokemon)(pokemon.get_name())
        self.pokedex.add(clone.get_name())
        self.pokemons.append(clone)
        clone.change_trainer(self)
        print("You have caught " + clone.get_name())

    def walk(self, direction):
        if (direction == 'w' and self.position[1] != 0):
            self.position[1] -= 1
            self.show_position()
        elif (direction == 'a' and self.position[0] != 0):
            self.position[0] -= 1
            self.show_position()
        elif (direction == 's' and self.position[1] != 1):
            self.position[1] += 1
            self.show_position()
        elif (direction == 'd' and self.position[0] != 1):
            self.position[0] += 1
            self.show_position()
        else:
            print("Invalid move!")

    def show_position(self):
        position = self.position
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
        self.name = name
        self.trainer = None
        #############################################################
        # Every Pokemon should have the following attributes:       #
        # 1) Health point                                           #
        # 2) Max health point                                       #
        # 3) Power point                                            #
        # 4) Max power point                                        #
        # 5) A list of moves                                        #
        # 6) A list containing the damage of the corresponding move #
        # "Struggle" is a default move that every Pokemon knows and #
        # is used only when the pp of every other move is 0.        #
        #############################################################
        self.hp = 100
        self.max_hp = self.hp
        self.pp = [0,]
        self.pp_full = [0,]
        self.move = ["Struggle",]
        self.damage = [7,]

    # Getters/Accessors
    def get_name(self):
        return self.name

    def get_trainer(self):
        return self.trainer

    def get_hp(self):
        return self.hp

    def get_pp(self):
        return self.pp

    def get_moves(self):
        return self.move

    def get_damage(self):
        return self.damage

    # Modifiers/Mutators
    def change_trainer(self, trainer):
        self.trainer = trainer

    def minus_hp(self, damage):
        ############################################################
        # Changes hp according to damage                           #
        #                                                          #
        # @params damage is an int indicating the amount of damage #
        ############################################################
        self.hp -= damage
        if (self.hp < 0):
            self.hp = 0

    def restore(self):
        self.hp = self.max_hp

    # Other methods
    def take_damage(self, hit):
        self.minus_hp(hit)
        print(self.get_name() + " has " + str(self.get_hp()) + " health left.")

    def attack(self, foe):
            print(self.get_name() + " use " + self.get_moves()[0] + ".")
            foe.take_damage(self.get_damage()[0])
            print(self.get_name() + " took recoil damage.")
            self.take_damage(5) # Recoil damage of Struggle is 5

        
class Type(Pokemon): # This is an abstract class (i.e. not meant to be instantiated)
    def __init__(self, name):
        super().__init__(name)

    def restore(self):
        ##########################################################
        # Restore the pp of this Pokemon and then restore the hp #
        ##########################################################
        self.pp = self.pp_full.copy()
        super().restore()

    def attack(self, foe, attack):
        ###################################################
        # Check if this Pokemon has any pp left:          #
        # If no pp left, use Struggle                     #
        # Else, use the attack chosen                     #
        #                                                 #
        # @params foe is the enemy Pokemon                #
        # @params attack is the index of move on the list #
        ###################################################
        pps = self.get_pp()
        if (pps[attack] > 0):
            print(self.get_name() + " use " + self.get_moves()[attack] + ".")
            foe.take_damage(self.get_damage()[attack])
            pps[attack] -= 1
        else:
            print(self.get_name() + " does not have PP left for any move.")
            super().attack(foe)

class Normal(Type):
    def __init__(self, name):
        super().__init__(name)
        self.move.append("Tackle")
        self.damage.append(10)
        self.pp_full.append(5)
        self.pp.append(5)
                                                     
class Grass(Type):
    def __init__(self, name):
        super().__init__(name)
        self.move.append("Razor Leaf")
        self.damage.append(15)
        self.pp_full.append(5)
        self.pp.append(5)
                                                     
class Electric(Type):
    def __init__(self, name):
        super().__init__(name)
        self.move.append("Thunderbolt")
        self.damage.append(15)
        self.pp_full.append(5)
        self.pp.append(5)
                                                     
class Water(Type):
    def __init__(self, name):
        super().__init__(name)
        self.move.append("Surf")
        self.damage.append(15)
        self.pp_full.append(5)
        self.pp.append(5)                                            

class Fire(Type):
    def __init__(self, name):
        super().__init__(name)
        self.move.append("Flamethrower")
        self.damage.append(20)
        self.pp_full.append(3)
        self.pp.append(3)

class Flying(Type):
    def __init__(self, name):
        super().__init__(name)
        self.move.append("Fly")
        self.damage.append(15)
        self.pp_full.append(5)
        self.pp.append(5)
