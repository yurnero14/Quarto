# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import logging
import argparse
import random
import quarto
from generate_agent import EvolvedAgent


class RandomPlayer(quarto.Player):
    """Random player"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        return random.randint(0, 15)

    def place_piece(self) -> tuple([int, int]):
        return random.randint(0, 3), random.randint(0, 3)

class ManualPlayer(quarto.Player):
    '''Manual player'''

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.quarto = quarto

    def choose_piece(self) -> int:
        return int(input())

    def place_piece(self) -> tuple([int, int]):
        return int(input()), int(input())


def main():
    agent_win = 0
    random_win = 0
    draw = 0
    iter = 500
    game = quarto.Quarto()
    GA_agent = EvolvedAgent(game)
    game.set_players((RandomPlayer(game), GA_agent))
    for _ in range(iter):
        game.reset()
        result = game.run()
        if result == -1:
            draw += 1
        elif result == 0:
            random_win += 1
        elif result == 1:
            agent_win += 1
    logging.warning(f"main: Winner: Agent won {agent_win} matches, Random won {random_win} and there were {draw} draws out of {iter}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase log verbosity')
    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        dest='verbose',
                        const=2,
                        help='log debug messages (same as -vv)')
    args = parser.parse_args()

    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)

    main()