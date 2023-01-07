from Pokemon_Part_4 import *
import random

def battle(pokemon, wild_pokemon, trainer):
    while (pokemon.get_hp() > 0 and wild_pokemon.get_hp() > 0):
        print("1. Attack")
        print("2. Catch")
        print("3. Run")
        option = int(input("What would you like to do? "))
        if (option == 1):
            pokemon.attack(wild_pokemon, random.randint(1, len(wild_pokemon.get_moves()) - 1))
            print()
            if (wild_pokemon.get_hp() <= 0):
                break
            else:
                wild_pokemon.attack(pokemon, random.randint(1, len(wild_pokemon.get_moves()) - 1))
                print()
        elif (option == 2):
            trainer.catch_pokemon(wild_pokemon)
            break
        else:
            break
        
    if (pokemon.get_hp() <= 0 and wild_pokemon.get_hp() <= 0):
        print("Both pokemons have fainted.")
    elif (pokemon.get_hp() <= 0):
        print(pokemon.get_name() + " has fainted.")
        print(wild_pokemon.get_name() + " wins.")        
    elif (wild_pokemon.get_hp() <= 0):
        print(wild_pokemon.get_name() + " has fainted.")
        print(pokemon.get_name() + " wins.")
        pokemon.increase_exp()
    pokemon.restore()
    wild_pokemon.restore()

def begin_game():
    print('Welcome to the world of Pokemon. You will be able to catch pokemons, train them and also engage in pokemon battles!\n')

    trainer_name = input('Before we start, what is your name?\n')
    trainer = Trainer(trainer_name)

    print('Okay', trainer.get_name(), 'let\'s go into the pokemon world!\n')
                    
    bulbasaur = Grass('Bulbasaur', [(Grass, "Ivysaur"), (Grass, "Venusaur")])
    pikachu = Electric('Pikachu', [(Electric, "Raichu")])
    tauros = Normal('Tauros', [])
    mudkip = Water('Mudkip', [(Water, "Marshtomp"), (Water, "Swampert")])
    squirtle = Water("Squirtle", [(Water, "Wartortle"), (Water, "Blastoise")])
    charmander = Fire("Charmander", [(Fire, "Charmeleon"), (FireFlying, "Charizard")])
    pidgey = Flying("Pidgey", [(Flying, "Pidgeotto"), (Flying, "Pidgeot")])
    charizard = FireFlying("Charizard", [])

    
    wild_pokemons = [bulbasaur, charmander, pikachu, tauros, squirtle, mudkip, pidgey]
    pokemon_count = len(wild_pokemons)
    for pokemon in wild_pokemons:
        pokemon_count += len(pokemon.get_evolution())

    starters = [bulbasaur, charmander, squirtle, pikachu]
    for i, pokemon in enumerate(starters):
        print(str(i + 1) + '. ' + pokemon.get_name())
    starter_pokemon = starters[int(input("Choose your starter pokemon: ")) - 1]
    trainer.catch_pokemon(starter_pokemon)
    wild_pokemons.remove(starter_pokemon)
    partition = [random.randint(0, len(wild_pokemons) - 1), random.randint(0, len(wild_pokemons) - 1), random.randint(0, len(wild_pokemons) - 1)]
    partition.sort()

    game_map = {(0, 0): Tile(wild_pokemons[0:partition[0]]),(0, 1): Tile(wild_pokemons[partition[0]:partition[1]]), (1, 0): Tile(wild_pokemons[partition[1]:partition[2]]), (1, 1): Tile(wild_pokemons[partition[2]:])}

    while (len(trainer.get_pokedex()) != pokemon_count):
        action(trainer, game_map)

    print("Congratulation, you are a Pokemon master!")

def action(trainer, game_map):
    print('''
What do you want to do now? Choose a number.
1. Move around
2. Encounter Pokemon
3. See Pokedex
4. Swap Pokemon
5. Evolve Pokemon''')
    option = int(input('Option number: '))

    if (option == 1):
        trainer.walk(next_move())
    elif (option == 2):
        trainer.encounter_pokemon(game_map[tuple(trainer.get_position())])
    elif (option == 3):
        pokedex = trainer.get_pokedex()
        if not pokedex:
            print("You have no pokemon.")
        else:
            for i, pokemon in enumerate(pokedex):
                print('#{:03d}: '.format(i + 1) + pokemon)
    elif (option == 4):
        trainer.swap_pokemon()
    elif (option == 5):
        evolve_pokemon(trainer)
    else:
        print('Invalid option!')

def next_move():
    print('''
Which direction would you like to move to?
1. Type 'w' to move to North
2. Type 'a' to move to the West
3. Type 's' to move to the South
4. Type 'd' to move to the East''')
    direction = input('Choose w, a, s or d: ')

    if direction not in ['a', 's', 'd', 'w']:
        print('Invalid direction')
        next_move()
    else:
        return direction

def evolve_pokemon(trainer):
    pokemons = trainer.get_pokemons()
    print()
    for i, pokemon in enumerate(pokemons):
        print(str(i + 1) + '. ' + pokemon.get_name())
    evolve = int(input("Which pokemon would you like to evolve? ")) - 1
    try:
        pokemons[evolve].evolve()
    except EvolveError as e:
        print(str(e))
    except ExpError as e:
        print(str(e))
    
begin_game()
