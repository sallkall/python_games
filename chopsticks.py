""" Game interface for Chopsticks
"""
from typing import List, Dict, Any
from game import GameState, Game

LEFT_HAND = 'l'
RIGHT_HAND = 'r'
ALL_HANDS = [LEFT_HAND, RIGHT_HAND]
PLAYERS = ['p1', 'p2']


class ChopsticksGameState(GameState):
    """
    Current state of the game for ChopsticksGame

    === Attributes ===
    player - the player currently playing the game (p1 or p2)
    hands - a dictionary containing information about
            the value each player's hands has
    """
    player: str
    hands: Dict[str, Dict[str, int]]

    def __init__(self, player: str, hands: Dict[str, Dict[str, int]]) -> None:
        """ Initialize the current state of the game

        >>> x = ChopsticksGameState('p1', {'p1': {'l': 1, \
        'r': 1}, 'p2': {'l': 1, 'r': 1}}).player
        'p1'
        >>> x = ChopsticksGameState('p1', {'p1': {'l': 1, \
        'r': 1}, 'p2': {'l': 1, 'r': 1}}).hands
        {'p1': {'LEFT_HAND': 1, 'RIGHT_HAND': 1}, \
        'p2': {'LEFT_HAND': 1, 'RIGHT_HAND': 1}}
        """
        super().__init__(player)
        self.hands = hands

    def __eq__(self, other: Any) -> bool:
        """ check if current game state is equal to other game state

        >>> x = ChopsticksGameState('p1', {'p1': {'l': 1, \
        'r': 1}, 'p2': {'l': 1, 'r': 1}})
        >>> y = ChopsticksGameState('p1', {'p1': {'l': 1, \
        'r': 1}, 'p2': {'l': 1, 'r': 1}})
        >>> x == y
        True
        """
        return (type(self) == type(other) and
                self.player == other.player and
                self.hands == other.hands)

    def get_current_hands(self) -> Dict[str, int]:
        """ Get the current hands in  the game

        >>> x = ChopsticksGameState('p1', {'p1': {'l': 1, \
        'r': 1}, 'p2': {'l': 1, 'r': 1}})
        >>> x.get_current_hands()
        {'LEFT_HAND': 1, 'RIGHT_HAND': 1}
        """
        return self.hands[self.get_current_player_name()]

    def get_possible_moves(self) -> List[object]:
        """ Return a list of all possible moves

        >>> x = ChopsticksGameState('p1', {'p1': {'l': 1, \
        'r': 1}, 'p2': {'l': 1, 'r': 1}})
        >>> x.get_possible_moves()
        ['ll', 'lr', 'rl', 'rr']
        """
        moves = []
        current_hands = self.get_current_hands()
        for from_hand in ALL_HANDS:
            if current_hands[from_hand] > 0:
                for to_hand in ALL_HANDS:
                    moves.append(from_hand + to_hand)
        return moves

    def get_hands_copy(self) -> Dict[str, Dict[str, int]]:
        """ A copy of dictionary

        >>> x = ChopsticksGameState('p1', {'p1': {'l': 1, \
        'r': 1}, 'p2': {'l': 1, 'r': 1}})
        >>> x.get_hands_copy()
        {'p1': {'l': 1, 'r': 1}, 'p2': {'l': 1, 'r': 1}}
        """
        copied_hands = {}
        for player in PLAYERS:
            copied_hands[player] = dict(self.hands[player])
        return copied_hands

    def make_move(self, move_to_make: str) -> GameState:
        """ Implement a move

        >>> x = ChopsticksGameState('p1', {'p1': {'l': 1, \
        'r': 1}, 'p2': {'l': 1, 'r': 1}})
        >>> move_to_make = 'll'
        >>> print(x.make_move(move_to_make))
        [player = p2, hands = p1: 1-1, p2: 2-1]
        """
        player = self.get_current_player_name()
        enemy = self.get_next_player()
        new_hands = self.get_hands_copy()
        new_hands[enemy][move_to_make[1]] = (new_hands[enemy][move_to_make[1]] +
                                             new_hands[player][
                                                 move_to_make[0]]) % 5
        return ChopsticksGameState(enemy, new_hands)

    def __str__(self) -> str:
        """ Return info about the state of the game in string format

        >>> x = ChopsticksGameState('p1', {'p1': {'l': 1, \
        'r': 1}, 'p2': {'l': 1, 'r': 1}})
        >>> print(x)
        [player = p1, hands = p1: 1-1,p2: 1-1]
        """
        hands_str = ', '.join(
            ['{}: {}-{}'.format(k, v[LEFT_HAND], v[RIGHT_HAND]) for k, v in
             self.hands.items()])
        return '[player = {}, hands = {}]'.format(self.player, hands_str)


class ChopsticksGame(Game):
    """
    Functions used to player Chopsticks Game

    === Attributs ===
    current_state - current game state
    """
    current_state: ChopsticksGameState

    def __init__(self, is_p1_turn: bool) -> None:
        """ Initialize super class

        >>> x = ChopsticksGame(True)
        >>> x.current_state.get_current_player_name() == 'p1'
        True
        """
        if is_p1_turn:
            player = PLAYERS[0]
        else:
            player = PLAYERS[1]

        hands = {}
        for p in PLAYERS:
            hands[p] = {}
            for hand in ALL_HANDS:
                hands[p][hand] = 1

        self.current_state = ChopsticksGameState(player, hands)

    def __str__(self) -> str:
        """ Return information of the current game in str format

        """
        return "Player 1: {}; Player 2: {}"\
            .format(self.current_state.hands['p1'],
                    self.current_state.hands['p2'])

    def __eq__(self, other: ChopsticksGameState) -> bool:
        """ Comapre whether the two game state are equal

        """
        return (type(self) == type(other) and
                self.current_state.player == other.player and
                self.current_state.hands == other.hands)

    def get_instructions(self) -> str:
        """ Return instructions for the game

        """
        return '1. Each of two players begins with one finger pointed up on' \
               'each of their hands.\n2. Player A touches one hand to one of ' \
               'Player B\'s hands, increasing the number of fingers pointing ' \
               'up on Player B\'s hand by the number on Player A\'s hand. ' \
               'The number pointing up on Player A\'s hand remains the same.' \
               '\n3. If Player B now has five fingers up, that hand becomes ' \
               '"dead" or unplayable. If the number of fingers should exceed ' \
               'five, subtract five from the sum.\n4. Now Player B touches ' \
               'one hand to one of Player A\'s hands, and the distribution ' \
               'of fingers proceeds as above, including the possibility of a ' \
               '"dead" hand.\n5. Play repeats steps 2-4 until some player has' \
               'two "dead" hands, thus losing.'

    def is_over(self, state: 'ChopsticksGameState') -> bool:
        """ Check and return is game is over
        """
        for player in PLAYERS:
            if state.hands[player][LEFT_HAND] == 0 and \
                            state.hands[player][RIGHT_HAND] == 0:
                return True

        return False

    def is_winner(self, player: str) -> bool:
        """ Check if player is the winner
        """
        enemy = GameState(player).get_next_player()
        return self.is_over(self.current_state)\
            and self.current_state.hands[enemy][LEFT_HAND] == 0 \
            and self.current_state.hands[enemy][RIGHT_HAND] == 0

    def str_to_move(self, move: str) -> Any:
        """ Retrun a move in int format
        """
        return move


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
