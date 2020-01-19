"""Stonehenge Game State
"""
import pprint
import string
from typing import List, Dict, Set

from game_state import GameState

NOT_USED = 'x'
P1_CLAIMED = '1'
P2_CLAIMED = '2'
NOT_CLAIMED = '@'


def indent(line, count) -> str:
    """ Helper function for the str method. Adds
    count mutiple of spaces before line

        >>> indent('FIVESPACES', 5)
        '     FIVESPACES'
        >>> indent('', 0)
        ''
    """
    return ' ' * count + line


def copy_nodes(nodes: List[List[str]]) -> List[List[str]]:
    """ Get a deep copy of a matrix / game grid

    >>> m = [['x', 'x', 'A', 'B'], ['x', 'C', 'D', 'E'], \
            ['F', 'G', 'H', 'I'], ['J', 'K', 'L', 'x']]
    >>> copy_nodes(m) == m
    True
    """
    return [list(line) for line in nodes]


def get_row_lines(nodes: List[List[str]]) -> List[List[str]]:
    """ Get the rows of a grid

    >>> m = [['x', 'A', 'B'], ['C', 'D', 'E'], ['F', 'G', 'x']]
    >>> get_row_lines(m)
    [['A', 'B'], ['C', 'D', 'E'], ['F', 'G']]
    """
    return [[cell for cell in line if cell != NOT_USED] for line in nodes]


def get_down_left_lines(nodes: List[List[str]]) -> List[List[str]]:
    """ Get the down left rows of a grid

    >>> m = [['x', 'A', 'B'], ['C', 'D', 'E'], ['F', 'G', 'x']]
    >>> get_down_left_lines(m)
    [['A', 'C'], ['B', 'D', 'F'], ['E', 'G']]
    """
    size = len(nodes)
    lines = []
    for sum_up in range(0, 2 * size - 2):
        line = []
        for i in range(sum_up + 1):
            j = sum_up - i
            add_to_line(nodes, i, j, line)
        ln = len(line)
        if ln > 0:
            lines.append(line)
    return lines


def get_down_right_lines(nodes: List[List[str]]) -> List[List[str]]:
    """ Get the down right rows of a grid

    >>> m = [['x', '1', '1'], ['C', 'D', 'E'], ['F', 'G', 'x']]
    >>> get_down_right_lines(m)
    [['C', 'F'], ['1', 'D', 'G'], ['1', 'E']]
    """
    size = len(nodes)
    lines = []
    for j in range(size):
        line = []
        for i in range(size):
            add_to_line(nodes, i, j, line)

        lines.append(line)
    return lines


def add_to_line(nodes: List[List[str]], x: int,
                y: int, line: List[str]) -> None:
    """ Helper function to assign value to lines
    """
    if x < 0 or x >= len(nodes):
        return
    if y < 0 or y >= len(nodes):
        return
    if nodes[x][y] == NOT_USED:
        return
    line.append(nodes[x][y])


def get_claimer(line: List[str]) -> str:
    """ Helper function to keep track of claimers (1 or 2)
    """
    counter = {P1_CLAIMED: 0, P2_CLAIMED: 0}
    for cell in line:
        if cell in counter:
            counter[cell] += 1
    max_player = get_max_by_value(counter)
    if max_player != NOT_CLAIMED and counter[max_player] >= len(line) / 2:
        return max_player
    return NOT_CLAIMED


def get_max_by_value(counter: Dict[str, int]) -> str:
    """ Comapare claimers to see which line is claimed by who
    """
    if counter[P1_CLAIMED] > counter[P2_CLAIMED]:
        return P1_CLAIMED
    elif counter[P2_CLAIMED] > counter[P1_CLAIMED]:
        return P2_CLAIMED
    return NOT_CLAIMED


def get_cell_sets(line: List[str]) -> Set[str]:
    """ Get the uncliamed cells in a line
    """
    return set([cell for cell in line if cell
                not in [P1_CLAIMED, P2_CLAIMED, NOT_USED]])


def get_update_lines(claim_marks: List[str], lines: List[List[str]]) -> list:
    """ Get updated row
    """
    updated = list(claim_marks)
    for i in range(len(lines)):
        if updated[i] == NOT_CLAIMED and get_claimer(lines[i]) != NOT_CLAIMED:
            updated[i] = get_claimer(lines[i])

    return updated


def create_start_henge_state(is_p1_turn: bool,
                             side_length: int) -> 'StoneHengeState':
    """ Generate the grid from side_length
    """
    size = side_length + 1
    nodes = [[''] * size for _ in range(size)]

    # fill in not used cells
    for i in range(size):
        for j in range(size):
            if i + j < size - 2:
                nodes[i][j] = NOT_USED
    nodes[-1][-1] = NOT_USED

    # fill in empty cells
    index = 0
    for i in range(size):
        for j in range(size):
            if nodes[i][j] != NOT_USED:
                nodes[i][j] = string.ascii_uppercase[index]
                index += 1

    return StoneHengeState(is_p1_turn, nodes,
                           [NOT_CLAIMED] * size, [NOT_CLAIMED] * size,
                           [NOT_CLAIMED] * size)


class StoneHengeState(GameState):
    """ Gamestate for stonehenge game
    """
    WIN: int = 1
    LOSE: int = -1
    DRAW: int = 0
    p1_turn: bool

    def __init__(self, is_p1_turn: bool, nodes: List[List[str]],
                 row_line_claimers: List[str], left_line_claimers: List[str],
                 right_line_claimers: List[str]) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        >>> m = [['x', 'A', 'B'], ['C', 'D', 'E'], ['F', 'G', 'x']]
        >>> s = StoneHengeState(True, m, ['@', '@', '@'], ['@', '@', '@'], ['@', '@', '@'])
        >>> s.nodes
        [['x', 'A', 'B'], ['C', 'D', 'E'], ['F', 'G', 'x']]
        """
        super().__init__(is_p1_turn)
        self.nodes = nodes
        self.row_line_claimers = row_line_claimers
        self.left_line_claimers = left_line_claimers
        self.right_line_claimers = right_line_claimers

    def make_move(self, move: str) -> 'StoneHengeState':
        """
        Return the GameState that results from applying move to this GameState.

        >>> m = [['x', 'A', 'B'], ['C', 'D', 'E'], ['F', 'G', 'x']]
        >>> new_m = [['x', '1', 'B'], ['C', 'D', 'E'], ['F', 'G', 'x']]
        >>> s = StoneHengeState(True, m, ['@', '@', '@'], ['@', '@', '@'], ['@', '@', '@'])
        >>> str(s.make_move('A')) == str(StoneHengeState(False, new_m, ['1', '@', '@'], ['1', '@', '@'], ['@', '@', '@']))
        True
        """
        # update nodes
        updated_nodes = copy_nodes(self.nodes)
        for i in range(len(updated_nodes)):
            for j in range(len(updated_nodes[i])):
                if updated_nodes[i][j] == move:
                    if self.p1_turn:
                        updated_nodes[i][j] = P1_CLAIMED
                    else:
                        updated_nodes[i][j] = P2_CLAIMED

        # update claimed lay lines
        claimed_row_lines = get_update_lines(
            self.row_line_claimers, get_row_lines(updated_nodes))
        claimed_left_lines = get_update_lines(
            self.left_line_claimers, get_down_left_lines(updated_nodes))
        claimed_right_lines = get_update_lines(
            self.right_line_claimers, get_down_right_lines(updated_nodes))

        return StoneHengeState(not self.p1_turn, updated_nodes,
                               claimed_row_lines,
                               claimed_left_lines, claimed_right_lines)

    def __str__(self) -> str:
        """
        Return a string representation of the current matrix of the game.

        >>> m = [['x', 'A', 'B'], ['C', 'D', 'E'], ['F', 'G', 'x']]
        >>> s = StoneHengeState(True, m, ['@', '@', '@'], ['@', '@', '@'], ['@', '@', '@'])
        >>> print(s)
                @   @
               /   /
          @ - A - B   @
             / \\ / \\ /
        @ - C - D - E
             \\ / \\ / \\
          @ - F - G   @
               \\   \\
                @   @
        """
        row_lines = get_row_lines(self.nodes)

        left_claimers = list(self.left_line_claimers)
        right_claimers = list(self.right_line_claimers)
        row_claimers = list(self.row_line_claimers)

        outputs = []

        # first two lines
        first_two_left_claimers, left_claimers = \
            left_claimers[:2], left_claimers[2:]
        outputs.append('   '.join(first_two_left_claimers))
        outputs.append('/   /')

        # body (before central row)
        for i in range(len(row_lines) - 1):
            row = row_lines[i]
            line = row_claimers[i] + ' - ' + ' - '.join(row)
            ln = len(left_claimers)
            if ln > 0:
                line += '   ' + left_claimers.pop(0)
            outputs.append(line)
            outputs.append(' '.join(['/ \\'] * len(row)) + ' /')

        # body (last row)
        row = row_lines[-1]
        outputs[-1] = ' '.join(['\\ /'] * len(row)) + ' \\'
        last_right_claimer = right_claimers.pop(-1)
        outputs.append('{} - {}   {}'.format(row_claimers[-1],
                                             ' - '.join(row),
                                             last_right_claimer))

        # last two lines
        outputs.append('   '.join(['\\'] * len(row)))
        outputs.append('   '.join(right_claimers))

        # add indents
        dec = True
        count = 4 + 2 * (len(self.nodes) - 1)
        for i in range(len(outputs)):
            if i % 2 == 0 and i != 0 and i != len(outputs) - 1:
                outputs[i] = indent(outputs[i], count - 4)
            else:  # link lines
                outputs[i] = indent(outputs[i], count)

            if count == 4:
                dec = False

            if dec:
                count -= 1
            else:
                count += 1

        return '\n'.join(outputs)

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).

        >>> m = [['x', 'A', 'B'], ['C', 'D', 'E'], ['F', 'G', 'x']]
        >>> s = StoneHengeState(True, m, ['@', '@', '@'], \
         ['@', '@', '@'], ['@', '@', '@'])
        >>> x = [['x', 'A', 'B'], ['C', 'D', 'E'], ['F', 'G', 'x']]
        >>> y = StoneHengeState(False, x, ['@', '@', '@'], \
        ['@', '@', '@'], ['@', '@', '@'])
        >>> repr(s) == repr(y)
        False
        """
        claimers = self.row_line_claimers + self.left_line_claimers \
                   + self.right_line_claimers
        return pprint.pformat(self.nodes) + pprint.pformat(self.p1_turn) \
               + pprint.pformat(claimers)

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.

        >>> m = [['x', 'A', 'B'], ['C', 'D', 'E'], ['F', 'G', 'x']]
        >>> s = StoneHengeState(True, m, ['@', '@', '@'], \
         ['@', '@', '@'], ['@', '@', '@'])
        >>> s.get_possible_moves()
        ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        """
        if self.get_winner():
            return []

        moves = []
        for row in self.nodes:
            for cell in row:
                if cell not in [NOT_USED, P1_CLAIMED, P2_CLAIMED]:
                    moves.append(cell)

        return moves

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.

        >>> m = [['x', 'A', 'B'], ['C', 'D', 'E'], ['F', 'G', 'x']]
        >>> s = StoneHengeState(True, m, ['@', '@', '@'], \
        ['@', '@', '@'], ['@', '@', '@'])
        >>> s.rough_outcome()
        1
        """
        if self.get_winner() == self.get_current_player_name():
            return 1
        if self.get_winner() and self.get_winner() \
                != self.get_current_player_name():
            return - 1

        for move in self.get_possible_moves():
            next_state = self.make_move(move)
            score = next_state.rough_outcome()
            if score == 1:
                return -1

        claimers = self.row_line_claimers + \
                   self.left_line_claimers + self.right_line_claimers
        counter = {P1_CLAIMED: 0, P2_CLAIMED: 0}
        for claimer in claimers:
            if claimer != NOT_CLAIMED:
                counter[claimer] += 1

        if self.p1_turn:
            key = P1_CLAIMED
        key = P2_CLAIMED

        return max([1, counter[key] / len(claimers) / 2]) * 2 - 1

    def get_winner(self):
        """ Check and return the name of the player who had won

        >>> m = [['x', '1', '1'], ['1', '1', '1'], ['1', '1', 'x']]
        >>> s = StoneHengeState(True, m, ['1', '1', '1'], \
        ['1', '1', '1'], ['1', '1', '1'])
        >>> s.get_winner()
        'p1'
        """
        claimers = self.row_line_claimers + \
                   self.left_line_claimers + self.right_line_claimers
        counter = {P1_CLAIMED: 0, P2_CLAIMED: 0}
        for claimer in claimers:
            if claimer != NOT_CLAIMED:
                counter[claimer] += 1

        # tie
        if counter[P1_CLAIMED] == counter[P2_CLAIMED] \
                and counter[P1_CLAIMED] == len(claimers) / 2:
            return None
        # p1 win
        elif counter[P1_CLAIMED] >= len(claimers) / 2:
            return 'p1'
        # p2 win
        elif counter[P2_CLAIMED] >= len(claimers) / 2:
            return 'p2'
        # game is not over
        return None


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
