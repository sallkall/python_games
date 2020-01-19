""" Parent class for game_interface
"""
from typing import List, Any
PLAYERS = ['p1', 'p2']


class GameState:
    """
    Super class of the state of the game
    === Attributes ===
    player - a string representing the name of the player
    """
    player: str

    def __init__(self, player: str) -> None:
        """ Initialize the current state of the class
        >>> GameState('p2').player
        'p2'
        """
        if player == 'p1' or player == 'p2':
            self.player = player

    def is_valid_move(self, move):
        """ Check if move_to_make is a valid move
        """
        return move and move in self.get_possible_moves()

    def get_possible_moves(self) -> List[object]:
        """ Return a list of all possible moves
        """
        raise NotImplementedError("Must implement in subclass")

    def get_current_player_name(self) -> str:
        """ Get the current player's name

        >>> x = GameState('p1')
        >>> x.get_current_player_name()
        'p1'
        >>> y = GameState('p2')
        >>> y.get_current_player_name()
        'p2'
        """
        return self.player

    def make_move(self, move_to_make) -> None:
        """ Implement a move
        """
        raise NotImplementedError("Must implement in subclass")

    def get_next_player(self):
        """ Helper function to get the name of the next player
        >>> x = GameState('p1')
        >>> x.get_next_player()
        'p2'
        >>> y = GameState('p2')
        >>> y.get_next_player()
        'p1'
        """
        index = PLAYERS.index(self.player)
        return PLAYERS[(index + 1) % len(PLAYERS)]


class Game:
    """
    Super Class of Games
    """

    def __init__(self) -> None:
        """ Initialize super class
        """
        self.current_state = None

    def __eq__(self, other: Any) -> bool:
        """ Check to se if self equals others
        """
        return (type(self) == type(other) and
                self.current_state == other.current_state)

    def get_instructions(self) -> str:
        """ Return instructions for the game
        """
        raise NotImplementedError("Must implement in subclass")

    def is_over(self, state: 'GameState') -> bool:
        """ Check and return is game is over
        """
        raise NotImplementedError("Must implement in subclass")

    def is_winner(self, player: str) -> bool:
        """ Check if player is the winner
        """
        raise NotImplementedError("Must implement in subclass")

    def str_to_move(self, move: str) -> int:
        """ Retrun a move in int format
        """
        raise NotImplementedError("Must implement in subclass")


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
