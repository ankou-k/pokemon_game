from Pokemon_Part_4_Game_File import *
import Pokemon_Part_4_Game_File as P4
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
        clone = type(pokemon)(pokemon.get_name(), pokemon.get_evolution())
        self.pokedex.add(clone.get_name())
        self.pokemons.append(clone)
        clone.change_trainer(self)
        print("You have caught " + clone.get_name())

    def encounter_pokemon(self, tile):
        wild_pokemon = tile.spawn_pokemon()
        if (wild_pokemon != None):
            print("\nA wild " + wild_pokemon.get_name() + " appeared.")
            P4.battle(self.get_pokemons()[0], wild_pokemon, self)

    def swap_pokemon(self):
        pokemons = self.get_pokemons()
        print()
        for i, pokemon in enumerate(pokemons):
            print(str(i + 1) + '. ' + pokemon.get_name())
        pokemon = pokemons.pop(int(input("Which pokemon would you like to switch? ")) - 1)
        pokemons.insert(int(input("Insert where? ")) - 1, pokemon)

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
    def __init__(self, name, evolution):
        self.name = name
        self.trainer = None
        self.hp = 1000
        self.max_hp = self.hp
        self.pp = [0,]
        self.pp_full = [0,]
        self.move = ["Struggle",]
        self.damage = [7,]
        self.evolution = evolution
        self.exp = 0

    # Getters/Accessors
    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_moves(self):
        return self.move

    def get_damage(self):
        return self.damage

    def get_trainer(self):
        return self.trainer

    def get_evolution(self):
        return self.evolution

    def get_exp(self):
        return self.exp

    # Modifiers/Mutators
    def change_trainer(self, trainer):
        self.trainer = trainer

    def minus_hp(self, damage):
        self.hp -= damage
        if (self.hp < 0):
            self.hp = 0

    def restore(self):
        self.hp = self.max_hp

    def increase_exp(self):
        self.exp += 1

    # Other methods
    def take_damage(self, hit):
        self.minus_hp(hit)
        print(self.get_name() + " has " + str(self.get_hp()) + " health left.")

    def attack(self, foe):
            print(self.get_name() + " use " + self.get_moves()[0] + ".")
            foe.take_damage(self.get_damage()[0])
            print(self.get_name() + " took recoil damage.")
            self.take_damage(5) # Recoil damage of Struggle is 5

    def evolve(self):
        evolution = self.get_evolution()
        if (evolution):
            if (self.exp < 5):
                raise ExpError(self)
            print(self.get_name() + " has evolved to " + evolution[0][1] + ".")
            evolution = evolution.pop(0)
            trainer = self.get_trainer()
            evolve_pokemon = evolution[0](evolution[1], self.get_evolution())
            evolve_pokemon.hp = int(1.2 * self.get_hp())
            evolve_pokemon.max_hp = evolve_pokemon.hp
            evolve_pokemon.change_trainer(trainer)
            trainer.pokedex.add(evolve_pokemon.get_name())
            trainer.get_pokemons().remove(self)
            trainer.get_pokemons().append(evolve_pokemon)
        else:
            raise EvolveError(self)
        
class Type(Pokemon): # This is an abstract class (i.e. not meant to be instantiated)
    def __init__(self, name, evolution):
        super().__init__(name, evolution)

    def get_pp(self):
        return self.pp

    def restore(self):
        self.pp = self.pp_full.copy()
        super().restore()

    def attack(self, foe, attack):
        pps = self.get_pp()
        if (pps[attack] > 0):
            print(self.get_name() + " use " + self.get_moves()[attack] + ".")
            foe.take_damage(self.get_damage()[attack])
            pps[attack] -= 1
        else:
            print(self.get_name() + " does not have PP left for any move.")
            super().attack(foe)

class Normal(Type):
    def __init__(self, name, evolution):
        super().__init__(name, evolution)
        self.move.append("Tackle")
        self.damage.append(10)
        self.pp_full.append(5)
        self.pp.append(5)
                                                     
class Grass(Type):
    def __init__(self, name, evolution):
        super().__init__(name, evolution)
        self.move.append("Razor Leaf")
        self.damage.append(15)
        self.pp_full.append(5)
        self.pp.append(5)
                                                     
class Electric(Type):
    def __init__(self, name, evolution):
        super().__init__(name, evolution)
        self.move.append("Thunderbolt")
        self.damage.append(15)
        self.pp_full.append(5)
        self.pp.append(5)
                                                     
class Water(Type):
    def __init__(self, name, evolution):
        super().__init__(name, evolution)
        self.move.append("Surf")
        self.damage.append(15)
        self.pp_full.append(5)
        self.pp.append(5)                                            

class Fire(Type):
    def __init__(self, name, evolution):
        super().__init__(name, evolution)
        self.move.append("Flamethrower")
        self.damage.append(50)
        self.pp_full.append(3)
        self.pp.append(3)

class Flying(Type):
    def __init__(self, name, evolution):
        super().__init__(name, evolution)
        self.move.append("Fly")
        self.damage.append(15)
        self.pp_full.append(5)
        self.pp.append(5)

class FireFlying(Fire, Flying):
    def __init__(self, name, evolution):
        super().__init__(name, evolution)

    def attack(self, foe, attack):
        moves = self.get_moves()
        pps = self.get_pp()
        if (sum(pps) == 0):
            super().attack(foe, "")
        else:
            print("What move do you want to use?")
            for i, move in enumerate(moves):
                if (i == 0):
                    continue
                else:
                    print(str(i) + ". " + move)
            option = int(input())
            if (option < 1 or option > (len(moves) - 1)):
                print("Invalid option!\n")
                return self.attack(foe, attack)
            elif (pps[option] == 0):
                print("No more pp for " + moves[option] + ".\n")
                return self.attack(foe, attack)
            else:
                super().attack(foe, option)

class EvolveError(Exception):
    def __init__(self, pokemon):
        self.pokemon = pokemon

    def __str__(self):
        return self.pokemon.get_name() + " cannot evolve further."

class ExpError(Exception):
    def __init__(self, pokemon):
        self.pokemon = pokemon

    def __str__(self):
        return "Not enough EXP, need " + str(5 - self.pokemon.get_exp()) + " more EXP."
