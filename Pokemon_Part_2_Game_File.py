from Pokemon_Part_2 import *
import sys, os
import random

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def battle(pokemon, wild_pokemon):
    while (pokemon.get_hp() > 0 and wild_pokemon.get_hp() > 0):
        pokemon.attack(wild_pokemon, random.randint(1, len(wild_pokemon.get_moves()) - 1))
        print()
        if (wild_pokemon.get_hp() <= 0):
            break
        else:
            wild_pokemon.attack(pokemon, random.randint(1, len(wild_pokemon.get_moves()) - 1))
            print()
        
    if (pokemon.get_hp() <= 0 and wild_pokemon.get_hp() <= 0):
        print("Both pokemons have fainted.")
    elif (pokemon.get_hp() <= 0):
        print(pokemon.get_name() + " has fainted.")
        print(wild_pokemon.get_name() + " wins.")        
    elif (wild_pokemon.get_hp() <= 0):
        print(wild_pokemon.get_name() + " has fainted.")
        print(pokemon.get_name() + " wins.")
    pokemon.restore()
    wild_pokemon.restore()

def test():
    ratata = Normal("Ratata")
    oddish = Grass("Oddish")
    pikachu = Electric("Pikachu")
    lapras = Water("Lapras")
    cyndaquil = Fire("Cyndaquil")
    dodrio = Flying("Dodrio")
    missingNo = Type("MissingNo")

    pokemons = [ratata, oddish, pikachu, lapras, cyndaquil, dodrio]

    print("Check moves:")
    for pokemon in pokemons:
        test = len(pokemon.get_moves()) == 2
        print(str(type(pokemon)) + ": " + str(test))
        if (not test):
            return

    print('\nCheck "Struggle":')
    for pokemon in pokemons:
        temp = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        for i in range(pokemon.get_pp()[1] + 1):
            pokemon.attack(missingNo, 1)
        sys.stdout = temp
        test = pokemon.get_hp() == 95
        print(str(type(pokemon)) + ": " + str(test))
        if (not test):
           return

    print("\nCheck restore health:")
    for pokemon in pokemons:
        pokemon.restore()
        test = pokemon.get_hp() == 100
        print(str(type(pokemon)) + ": " + str(test))
        if (not test):
            return

    print("\nCheck restore pp:")
    for pokemon in pokemons:
        pokemon.restore()
        temp = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        for i in range(pokemon.get_pp()[1] + 1):
            pokemon.attack(missingNo, 1)
        pokemon.restore()
        for i in range(pokemon.get_pp()[1] + 1):
            pokemon.attack(missingNo, 1)
        pokemon.restore()
        sys.stdout = temp
        test = sum(pokemon.get_pp()) > 0
        print(str(type(pokemon)) + ": " + str(test))
        if (not test):
            return
        
    for i in range(len(pokemons) // 2):
        pokemon_1, pokemon_2 = pokemons[2 * i], pokemons[2 * i + 1]
        print("\n=======================================================================")
        print("Battle No. " + str(i + 1) + ": " + pokemon_1.get_name() + " VS " + pokemon_2.get_name())
        input("Press 'Enter' to continue.\n")
        battle(pokemon_1, pokemon_2)
        
test()
