import extendedQuarto
from rl import *
from main import RandomPlayer
from quarto import Player
import logging
from trained_rl import TrainedRL
from opponent_agents import DumbAgent
from ga_agent import *
from tqdm import tqdm
from ga_dumb import UntrainedGAAgent
from ga_less_dumb import LeastDumbAgent

def train_q_learner(game: extendedQuarto.ExtendedQuarto, q_learner: RLPlayer, external_agent: Player, q_learner_turn: int) -> int:
    '''
    Function to run a game between the Q-Learner and an opponent agent
    '''
    
    player = 0
    winner = -1

    if(q_learner_turn == 0):
        is_q_learner = True
        players = (q_learner, external_agent)
        q_learner_player = 0
    else:
        is_q_learner = False
        players = (external_agent, q_learner)
        q_learner_player = 1
    
    
    while not game.check_finished() and game.check_winner() == -1: 
        
        piece_ok = False
        
        while not piece_ok: 
            piece_ok = game.select(players[player].choose_piece())
    
        piece_ok = False
   
        if player == 0: #switch players
            player = 1
            game.set_current_player(1)
            if(q_learner_player == 1):
                is_q_learner = True
            else:
                is_q_learner = False
        else: 
            player = 0
            game.set_current_player(0)
            if(q_learner_player == 0):
                is_q_learner = True
            else:
                is_q_learner = False
        
        if (is_q_learner == True):
            q_learner.update_q()

       
        while not piece_ok:
            x, y = players[player].place_piece()
            piece_ok = game.place(x, y)
    

        winner = game.check_winner()

    
    if (winner != q_learner_turn): # q-learner didn't win
        if (winner == -1): # draw
            q_learner.update_when_draw() 
        else:
            q_learner.update_when_lost()

    q_learner.clear_previous_vars()
    return winner


learning_rate = 0.8
discount_rate = 0.2
exploration_rate = 0.7

def q_learning_strategy(game: extendedQuarto.ExtendedQuarto, q_learner: RLPlayer, num_games: int):
    '''
    Strategy for making q-learner learn. Q-learner plays first against Dumb and then against Random
    Progression of difficulty
    '''
    # creat trained GA
    trained_evolved = EvolvedAgent(game) # performs better as second
    plus_pick_025 = (0.06369372715277863, 0.8847749515760825, 0.051531321271138734)
    plus_place_025 = (0.5117837231872915, 3.563965752635712e-05, 0.00032016772834300385, 0.07394996224198032, 0.38933362248027764, 0.024576884704581324)
    set_pick_and_place(trained_evolved, plus_pick_025, plus_place_025)

    results = []
    OPPONENTS = [DumbAgent(game), RandomPlayer(game), UntrainedGAAgent(game), LeastDumbAgent(game), EvolvedAgent(game), trained_evolved]

    for opponent in OPPONENTS:
        game.set_players((opponent, q_learner))
        won = 0
        lost = 0
        draw = 0
        games_run = 0 
        q_learner.exploration_rate = exploration_rate
        print("HERE", q_learner.exploration_rate)

        for _ in tqdm(range(num_games)):
            game.reset()

            if (q_learner.exploration_rate >= 0.2): # change the exploration rate to do more exploitation the more we play
                if (games_run == 300):
                    q_learner.exploration_rate -= 0.05 # migt end up in local optima

            q_learner_turn = 1
            winner = train_q_learner(game, q_learner, opponent, q_learner_turn)
            if (winner == q_learner_turn):
                results.append("won")
               
            elif (winner == -1):
                results.append("draw")
            
            else:
                results.append("lost")
            
            games_run += 1

        num_games += 700
        print(num_games)

        for result in results:
            if result == "draw":
                draw += 1
            elif result == "lost":
                lost += 1
            else:
                won += 1

        #prints results 
        print("Won: " + str(won))
        print("Lost: " + str(lost))
        print("Draw: " + str(draw))

        won = 0
        lost = 0
        draw = 0
        results = []
       

    return won, lost, draw #returns results


def run():
    '''
    Runs everything
    '''
    logging.getLogger().setLevel(level=logging.INFO)

    game_train = extendedQuarto.ExtendedQuarto()
    q_learner = RLPlayer(game_train, learning_rate, discount_rate, exploration_rate)
    
    q_learning_strategy(game_train, q_learner, 3000)

    q_learner.save_q_table() #saves table after training q-learner
    # q_table_1: num_games = 1000, games added per opponent = 500, exploration rate = decreases by 0,05 every 100th game
    # q_table_2: num_games = 2000, games added per opponent = 700, exploration rate = decreases by 0,05 every 200th game
    # q_table_3: num_games = 3000, games added per opponent = 700, exploration rate = decreases by 0,05 every 300th game

    
run()