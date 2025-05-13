# Computational Intelligence - Quarto

## TL;DR
Technologies: Python, NumPy, Jupyter Notebook, Q-Learning, Genetic Algorithms, Object-Oriented Design, Pickle, Git LFS; \
\
Designed and implemented AI agents to play the board game Quarto, applying advanced techniques in reinforcement learning and evolutionary algorithms. Tackled agent design, training optimization, and state-action encoding in a complex multi-state game environment.
- Developed and trained a Q-learning agent with a custom Q-table architecture integrating game state and action as a hashable key
- Designed sub-optimal "bad agents" to bootstrap RL training before transitioning to randomized or strategic opponents
- Implemented hash and equality methods for custom Q-table keys to overcome Python object comparison limitations
- Integrated Q-table persistence using Pickle, and optimized storage using Git LFS to handle large file sizes
- Created an ExtendedQuarto class to manage dynamic game states and agent evaluation across multiple training runs
- Collaborated on development and tuning of Genetic Algorithm-based agents for comparative evaluation
- Fine-tuned agent performance across 1000–3000+ training episodes, with exploration decay strategies and agent matchup variation


## Author
Muhammad Sarib Khan 

## Collaborators
Angelica Ferlin - Discussed possible solutions/problems and helped me with the management of Q tables. Also developed Genetic Algorithm Agents

## Resources 
### Links
- https://stackoverflow.com/questions/10016352/convert-numpy-array-to-tuple - If there's an error with the Q-table because numpy arrays are not hashable, you can resolve it by converting the numpy array into a tuple. 
- https://stackoverflow.com/questions/4901815/object-of-custom-type-as-dictionary-key - I've found a solution for QTableKey here, where instead of using a tuple, an object is used as the key.
- https://realpython.com/python-is-identity-vs-equality/  - I encountered a memory issue with the QTableKey, and this link clarified that I needed to implement an __eq__() method to enable comparison when hashing.


## Code Development
In the beginning of the project, I, with the help of Angelica did some research on different possible algorithms. However, after careful consideration, it was decided to implement Reinforcement Learning instead. I took this decision because I am much more confident implementing an RL based solution since I have done a few mini projects on my own in the past based on RL. Additionally, it was anticipated that Minimax would require a significant amount of time, given the large number of possible states in the game of Quarto.

In the process of developing the Reinforcement Learning strategy, a substantial amount of knowledge was gained from the concerned lectures. In all honesty, I am not the best in coding so Angelica helped giving me the direction to develop an algorithm to code for Q-learning.

Regarding the Q-table, the decision was made to combine the selected piece and the placement of the piece into a single move. Consequently, the key for the Q-table was structured as a tuple, incorporating both the current state (comprising the board array and the chosen piece) and the move itself. The Q-values were then associated with this key. To make the current state usable as part of the key, specific hash and equality (eq) functions had to be implemented. This approach was derived from a previously mentioned source.

In addition, following the creation of the RL agent with the goal of training it, another agent was intentionally designed to make poor decisions. This deliberate choice allowed the agent to undergo initial training with the "bad" agent before transitioning to random actions, thereby smoothing the overall learning process.
 
The ExtendedQuarto class was developed to enhance the integration of the custom-written code with the provided libraries. This class facilitated the ability to switch the current player, a critical aspect for the implemented logic and auxiliary functions to function smoothly.


Following the agent's training, the program stores the results in a file. This document is subsequently utilized by the trained agent class to read the Q-table and apply moves based on the knowledge acquired during training. Unfortunately, some setbacks were encountered due to the size of the file and using the pickle library. This library was generating a file that was too big to simply upload it on github. Hence, by using HFL (Large File Storage), a solution was found.


In addition, in order to get these results, the agent was trained with Genetic Algorith.

## Code Map 
- *extendedQuarto.py* -  An extended version of Quarto was created to incorporate additional functionality and features.
- *testQuarto.py* - An extended version of Quarto was developed to enable more comprehensive move testing and evaluation.
- *rl.py* - A Reinforcement Learning Agent and a corresponding Class designed to be used as a Key for the Q-table were implemented in the project.
-  *opponent_agents.py* - An intentionally designed agent was created to deliberately make suboptimal decisions as part of the training or testing process.
- *train_q_learner.py* -  includes a function that facilitates running a game between the Q-Learner and an opponent agent. Additionally, there's a strategy in place to guide the Q-Learner's learning process during these games.
- *trained_rl.py* - Class including the trained RL
- *q_table_1.pickle* - The Q-table is saved in a file with the following parameters: 
  - Number of games played: 1000
  - Games added per opponent: 500
  - Exploration rate decreases by 0.05 every 100th game.
- *q_table_2.pickle* - The Q-Learner is saved in a file with the specified parameters: 
  - Number of games played: 2000
  - Games added per opponent: 700
  - Exploration rate decreases by 0.05 every 200th game.
- *q_table_3.pickle* - The Q-Learner is saved in a file with the following parameters:
  - Number of games played: 3000
  - Games added per opponent: 700
  - Exploration rate decreases by 0.05 every 300th game.
    
## How to run the code
- In train_q_learner.py file, number of games can be set at line 158 of the file (3rd parameter). At line 108, the number of games after which you want to decrease exploration rate can be change
- In rl.py, at line 273, name the pickle file you want to save the q-table in
- in trained_rl, at line 64, keep the name of the file to read same as the last bullet point
- run python main.py

