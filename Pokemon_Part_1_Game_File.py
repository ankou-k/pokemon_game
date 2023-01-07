from Pokemon_Part_1 import *
import random

def begin_game():
    print('Welcome to the world of Pokemon. You will be able to catch pokemons, train them and also engage in pokemon battles!\n')

    trainer_name = input('Before we start, what is your name?\n')
    trainer = Trainer(trainer_name)

    print('Okay', trainer.get_name(), 'let\'s go into the pokemon world!\n')
                    
    bulbasaur = Pokemon('Bulbasaur')
    pikachu = Pokemon('Pikachu')
    tauros = Pokemon('Tauros')
    mudkip = Pokemon('Mudkip')
    squirtle = Pokemon("Squirtle")
    charmander = Pokemon("Charmander")
    pidgey = Pokemon("Pidgey")

    wild_pokemons = [bulbasaur, charmander, pikachu, tauros, squirtle, mudkip, pidgey]
    starters = [bulbasaur, charmander, squirtle, pikachu]
    for i, pokemon in enumerate(starters):
        print(str(i + 1) + '. ' + pokemon.get_name())
    starter_pokemon = starters[int(input("Choose your starter pokemon: ")) - 1]
    trainer.catch_pokemon(starter_pokemon)
    wild_pokemons.remove(starter_pokemon)
    partition = [random.randint(0, len(wild_pokemons) - 1), random.randint(0, len(wild_pokemons) - 1), random.randint(0, len(wild_pokemons) - 1)]
    partition.sort()

    game_map = {(0, 0): Tile(wild_pokemons[0:partition[0]]),(0, 1): Tile(wild_pokemons[partition[0]:partition[1]]), (1, 0): Tile(wild_pokemons[partition[1]:partition[2]]), (1, 1): Tile(wild_pokemons[partition[2]:])}

    while (len(trainer.get_pokedex()) != len(wild_pokemons)):
        action(trainer, game_map)

    print("Congratulation, you are a Pokemon master!")

def action(trainer, game_map):
    print("""
What do you want to do now? Choose a number.
1. Move around
2. Catch Pokemon
3. See Pokedex""")
    option = int(input('Option number: '))

    if (option == 1):
        trainer.show_position()
        trainer.walk(next_move())
    elif (option == 2):
        pokemon = game_map[tuple(trainer.get_position())].spawn_pokemon()
        if (pokemon):
            trainer.catch_pokemon(pokemon)
    elif (option == 3):
        pokedex = trainer.get_pokedex()
        if not pokedex:
            print("You have no pokemon.")
        else:
            for i, pokemon in enumerate(pokedex):
                print('#{:03d}: '.format(i + 1) + pokemon)
    else:
        print('Invalid option!')

def next_move():
    print("""
Which direction would you like to move to?
1. Type 'w' to move to North
2. Type 'a' to move to the West
3. Type 's' to move to the South
4. Type 'd' to move to the East""")
    direction = input('Choose w, a, s or d: ')

    if direction not in ['a', 's', 'd', 'w']:
        print('Invalid direction')
        next_move()
    else:
        return direction

begin_game()
