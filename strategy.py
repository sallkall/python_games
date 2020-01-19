"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any, Dict, List
from game import Game
from game_state import GameState

# TODO: Adjust the type annotation as needed.


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2 # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


def get_score(game: 'Game', state: 'GameState', player: str) -> int:
    """ Get score of the state
    """
    game.current_state = state
    if game.is_winner(player):
        return GameState.WIN
    return GameState.LOSE


def recursive_minimax_scores(game: 'Game', state: 'GameState',
                             player: str) -> Any:
    """ Find a move that produces a 'highest guaranteed score' at each step
        for the current player.
    """
    # base case
    if game.is_over(state):
        return get_score(game, state, player)

    # recursion over all possible scores in next states
    scores = [recursive_minimax_scores(game, state.make_move(move), player)
              for move in state.get_possible_moves()]

    if state.get_current_player_name() == player:
        return max(scores)
    return min(scores)


def recursive_minimax(game: 'Game') -> Any:
    """ Find the best possible move recursively
    """
    state = game.current_state
    moves = [(move, recursive_minimax_scores(game, state.make_move(move),
                                             state.get_current_player_name()))
             for move in state.get_possible_moves()]
    # find best move:
    best_move = None
    top_score = -2
    for move, score in moves:
        if score > top_score:
            best_move = move
            top_score = score
    return best_move


# Iterative Strategy:


class GameTreeNode(object):
    """ Class of GameTree with state as nodes
    """
    def __init__(self, game: Game, state: GameState, player: str):
        """ A Tree class with game state as nodes
        """
        self.game = game
        self.state = state
        self.player = player

    def children(self) -> List['GameTreeNode']:
        """ Return a list of children states from a node
        """
        return [GameTreeNode(self.game, self.state.make_move(move), self.player)
                for move in self.state.get_possible_moves()]

    def get_score(self, evaluated_state: Dict[str, int]) -> Any:
        """ Get the score of the state if it is evaluted and add too the stack
            (evaluated_state) If the children are not evaluated dont do anything
            After adding to the stack return the score that will maximize
            chance of wining for the player
        """
        children = self.children()
        scores = []
        for child in children:
            if str(child.state) not in evaluated_state:
                return None
            else:
                scores.append(evaluated_state[str(child.state)])
        scores.sort()
        if self.state.get_current_player_name() == self.player:
            return scores[-1]
        return scores[0]


def _evaluate_and_add(node: GameTreeNode, stack: List[GameTreeNode],
                      evaluated_state: Dict[str, int]):
    """ If the node had been evaluated get the score of the game and assign
        it to the according key in the stack
    """
    if node.game.is_over(node.state):
        score = get_score(node.game, node.state, node.player)
        evaluated_state[str(node.state)] = score
    else:
        score = node.get_score(evaluated_state)
        if score is not None:
            evaluated_state[str(node.state)] = score
        else:
            stack.append(node)


def iterative_minimax_strategy(game: Any) -> Any:
    """ Iterative minimax strategy for game
    """
    state = game.current_state
    player = state.get_current_player_name()
    moves = [(move, GameTreeNode(game, state.make_move(move), player))
             for move in state.get_possible_moves()]
    stack = [move[1] for move in moves]
    evaluated_state = {}  # game state string: score

    stack_length = len(stack)
    while stack_length > 0:
        node = stack.pop()
        _evaluate_and_add(node, stack, evaluated_state)

        not_evaluated = [n for n in node.children() if str(n.state)
                         not in evaluated_state]
        for n in not_evaluated:
            _evaluate_and_add(n, stack, evaluated_state)

    moves.sort(key=lambda item: evaluated_state[str(item[1].state)])
    return moves[-1][0]


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
