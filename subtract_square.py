""" Game interface for Subtract_Sqaure
"""
from typing import List, Any
from game import Game, GameState


class SubtractSquareGameState(GameState):
    """
    The state of game of SubtractSquareGame

    === Attributes ===
    player - the player currently playing the game (p1 or p2)
    number - the initial/starting value of the game
    """
    player: str
    number: int

    def __init__(self, player: str, number: int) -> None:
        """ Initialize the current state of the class
        >>> SubtractSquareGameState('p1', 20).player
        'p1'
        >>> SubtractSquareGameState('p1', 20).number
        20
        """
        super().__init__(player)
        self.number = number

    def __str__(self):
        """ Return string repersentation of
        >>> x = SubtractSquareGameState('p1', 20)
        >>> print(x)
        [player = p1, number = 20]
        """
        return '[player = {}, number = {}]'.format(
            self.get_current_player_name(), self.number)

    def __eq__(self, other) -> bool:
        """ Check if self and others are the same
        >>> x = SubtractSquareGameState('p1', 20)
        >>> y = SubtractSquareGameState('p1', 20)
        >>> x == y
        True
        """
        return (type(self) == type(other) and
                self.player == other.player and
                self.number == other.number)

    def get_possible_moves(self) -> List[object]:
        """ Return a list of all possible moves

        >>> g = SubtractSquareGameState('p1', 20)
        >>> g.get_possible_moves()
        [1, 4, 9, 16]
        >>> x = SubtractSquareGameState('p2', 10)
        >>> x.get_possible_moves()
        [1, 4, 9]
        """
        i = 1
        moves = []
        while i ** 2 <= self.number:
            moves.append(i ** 2)
            i += 1
        return moves

    def make_move(self, move_to_make: int) -> GameState:
        """ Implement a move

        >>> x = SubtractSquareGameState('p1', 20)
        >>> print(x.make_move(4)) == print(SubtractSquareGameState('p2', 16))
        [player = p2, number = 16]
        [player = p2, number = 16]
        True
        """
        next_player = self.get_next_player()
        return SubtractSquareGameState(next_player, self.number - move_to_make)


class SubtractSquareGame(Game):
    """
    Functions used to player SubtractSquare Game

    === Attributes ===
    current_state - current state of the game
    """
    current_state = SubtractSquareGameState

    def __init__(self, is_p1_turn: bool) -> None:
        """ Initialize super class
        """
        if is_p1_turn:
            player = 'p1'
        else:
            player = 'p2'

        number = int(input('Please choose a number: '))
        self.current_state = SubtractSquareGameState(player, number)

    def __str__(self) -> str:
        """ Return information of the current game in str format
        """
        return "The current value is: {}"\
            .format(self.current_state.number)

    def __eq__(self, other: SubtractSquareGameState) -> bool:
        """ Comapre if current game is equal to other games
        """
        return type(self) == type(other)

    def get_instructions(self) -> str:
        """ Return instructions for the game
        """
        instructions = \
            "To start the game please choose a staring value that is a" \
            "non-neative whole number\nDuring the player's turn choose" \
            "square of a positive whole number to subtract from the value" \
            "(iff the chosen square is not larger).\nAfter subtracting the" \
            "value will be updated and the next player chooses a square" \
            "to subtract from it.\nGame continues to alternate between" \
            "the two players until there ar eno more moves are possible." \
            "\nWho ever is about to play at this point loses."

        return instructions

    def is_over(self, state: 'GameState') -> bool:
        """ Check and return is game is over
        """
        return len(state.get_possible_moves()) == 0

    def is_winner(self, player: str) -> bool:
        """ Return the winner of the game (p1 or p2)
        """
        return (self.is_over(self.current_state) and
                self.current_state.get_current_player_name() != player)

    def str_to_move(self, move: str) -> Any:
        """ Retrun a move in int format
        """
        return int(move)


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
