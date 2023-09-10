from generate_agent import EvolvedAgent
import quarto
import random
import itertools

def fitness(individuals: list, game: quarto.Quarto, num_games: int) -> list:
    '''The fitness is determined as the number of wins in case of a tie the number of draws 
    between two individuals. The function thus lets all individuals play eachother num_games
    number of games and stores (win, draw) in a tuple and returns a list containing all 
    individuas and the respective fitness'''

    # Create a dict for each individual to store the score
    individual_score = {}
    for individual in individuals:
        individual_score[individual] = [0, 0]

    # Let all individuals play against each other num_games number of times to determine the fitness 
    # of each individual
    for individual_1, individual_2 in itertools.combinations(individuals, 2):
        
        play_1_win, play_2_win, draw = gameplay(individual_1, individual_2, game, num_games)

        # Store the score for each individual
        individual_score[individual_1][0] += play_1_win
        individual_score[individual_1][1] += draw
        individual_score[individual_2][0] += play_2_win
        individual_score[individual_2][1] += draw

        # Store the individual and it's corresponding score together
        individuals_and_score = []
        for individual in individuals:
            score = individual_score[individual]
            individuals_and_score.append([score, individual])

    return individuals_and_score

def gameplay(individual_1: EvolvedAgent, individual_2: EvolvedAgent, game: quarto.Quarto, num_games: int) -> tuple:
    # Keep track of the result of each match
    draw = 0
    play_1_win = 0
    play_2_win = 0

    # Set players
    game.set_players((individual_1, individual_2))

    # Play num_games games between each individual pair
    for _ in range(num_games):
        game.reset()
        result = game.run()
        if result == -1:
            draw += 1
        elif result == 0:
            play_1_win += 1
        elif result == 1:
            play_2_win += 1
    
    return (play_1_win, play_2_win, draw)
    
def population_init(mu: int, game: quarto.Quarto) -> list:
    '''Initialize the population'''
    individuals = []

    for i in range(mu):
        individuals.append(EvolvedAgent(game))
    
    individuals = fitness(individuals, game, 1)
    return individuals

def roulette(individuals: list) -> EvolvedAgent:
    '''The roulette gives an individual a chance to be selected as a parent in relation to it's fitness'''

    tot_wins = 0
    # Calculate the sum of all wins
    for individual in individuals:
        tot_wins += individual[0][0]
    
    # Spin the wheel, i.e. generate a random number between 0 and tot_wins to find out the winner
    parent_val = random.randint(0, tot_wins)

    for individual in individuals:
        if parent_val <= individual[0][0]:
            return individual[1]
        else:
            parent_val -= individual[0][0]

def offspring(individuals: list, game: quarto.Quarto, mutation: int) -> list:
    '''Generate offspring of the population'''

    offspring = []

    for i in range(int(len(individuals)/2)):
        p1 = roulette(individuals)
        p2 = roulette(individuals)

        # Generate children
        child1, child2 = crossover(p1, p2, game)

        # Mutation 
        if random.random() <= mutation:
            mutate(child1)

        if random.random() <= mutation:
            mutate(child2)

        # Add the children to the offspring
        offspring.append(child1)
        offspring.append(child2)
    
    return offspring
        

def mutate(individual: EvolvedAgent):
    '''Mutate the individual'''
    
    # Determine what picking and placing rule to mutate
    pick_rule = random.randint(0,2)
    place_rule = random.randint(0,5)

    # change said rules
    pick_val = list(individual.get_pick_prob())
    pick_val[pick_rule] = random.random()

    place_val = list(individual.get_place_prob())
    place_val[place_rule] = random.random()

    set_pick_and_place(individual, pick_val, place_val)

def crossover(p1: EvolvedAgent, p2: EvolvedAgent, game: quarto.Quarto) -> tuple:
    '''Creates two children to two parents'''
    pick_cross = random.randint(0, 3)
    place_cross = random.randint(0, 6)

    parent_1 = p1.get_pick_prob()
    parent_2 = p2.get_pick_prob()
    child_1_pick = []
    child_2_pick = []
    child_1_place = []
    child_2_place = []

    for i in range(pick_cross):
        child_1_pick.append(parent_1[i])
        child_2_pick.append(parent_2[i])

    for i in range(3 - pick_cross):
        child_1_pick.append(parent_2[i+pick_cross])
        child_2_pick.append(parent_1[i+pick_cross])

    parent_1 = p1.get_place_prob()
    parent_2 = p2.get_place_prob()

    for i in range(place_cross):
        child_1_place.append(parent_1[i])
        child_2_place.append(parent_2[i])

    for i in range(6 - place_cross):
        child_1_place.append(parent_2[i+place_cross])
        child_2_place.append(parent_1[i+place_cross])

    child_1 = EvolvedAgent(game)
    child_2 = EvolvedAgent(game)

    set_pick_and_place(child_1, child_1_pick, child_1_place)
    set_pick_and_place(child_2, child_2_pick, child_2_place)

    return child_1, child_2


def set_pick_and_place(individual: EvolvedAgent, pick_prob: list, place_prob: list):
    '''Sets the probabilites of pick and place according to the parameter values'''

    # Normalize the rules
    pick = [prob/sum(pick_prob) for prob in pick_prob]
    place = [prob/sum(place_prob) for prob in place_prob]

    individual.set_pick_prob_1(pick[0])
    individual.set_pick_prob_2(pick[1])
    individual.set_pick_prob_3(pick[2])

    individual.set_place_prob_1(place[0])
    individual.set_place_prob_2(place[1])
    individual.set_place_prob_3(place[2])
    individual.set_place_prob_4(place[3])
    individual.set_place_prob_5(place[4])
    individual.set_place_prob_6(place[5])

def run_evolution():
    '''This function runs the evolution algorithm in order to obtain the best agent'''

    # Initial parameters
    mu = 10
    mutate_rate = 0.25
    iterations = 100
    game = quarto.Quarto()

    individuals = population_init(mu, game)

    for _ in range(iterations):
        print("Iteration: " + str(_))

        # Generate offspring
        offspring_individuals = offspring(individuals, game, mutate_rate)

        # Combine the offspring with the initial population
        for individual in individuals:
            offspring_individuals.append(individual[1])

        # Determine fitness of said offspring
        individuals = fitness(offspring_individuals, game, 1)

        # Choose the mu best individuals and keep going to the next iteration
        individuals.sort(key = lambda x: x[0], reverse=True)
        individuals = individuals[0:mu]

    # Determine the fitness one last time, this time with 10 matches against each agent to 
    # reduce some of the variance in each game
    final_individuals = []
    for individual in individuals:
        final_individuals.append(individual[1])

    individuals = fitness(final_individuals, game, 10)
    individuals.sort(key = lambda x: x[0], reverse=True)
    return individuals


if __name__ == "__main__":
    individuals = run_evolution()
    best_agent = individuals[0][1]
    print(best_agent)