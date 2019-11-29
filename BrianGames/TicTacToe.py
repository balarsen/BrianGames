import numpy as np
import pandas as pd


class Move(object):
    """
    a class to contain a move and then play it on the board
    """

    @classmethod
    def randomMove(cls, board):
        """
        return a random move for the correct player
        :param board:
        :return:
        """
        turn = board.whoseTurn()
        moves = board.availableSquares()
        move = np.random.randint(0, len(moves))
        return cls(moves[move], turn, board)

    def __init__(self, ind, chr, board):
        self.ind = ind
        self.chr = chr
        self.board = board
        for v in self.ind:
            if v not in (0, 1, 2):
                raise ValueError("Invalid move specification (0,1,2)")
        if self.chr not in ('X', 'O'):
            raise ValueError("Invalid character in move (X,O)")
        if not isinstance(self.board, Board):
            raise ValueError("Invalid Board passed in")

    def checkAvailiable(self):
        """
        check that the proposed move is available on the board
        :param board:
        :return: True-available, False-non-available
        """
        return self.ind in self.board.availableSquares()

    def __str__(self):
        return "{}:({},{})".format(self.chr, *self.ind)

    __repr__ = __str__

    def __hash__(self):
        return hash(str(self))


class Board(object):
    """
    a board for tic-tac-toe

    has to provide a hash and if anyone has won
    """

    def __init__(self):
        """
        create an empty board
        """
        self.board = [['~', '~', '~'],
                      ['~', '~', '~'],
                      ['~', '~', '~']]

    def __hash__(self):
        return hash(str(self.board))

    def __str__(self):
        return "{}\n{}\n{}".format(*self.board)

    __repr__ = __str__

    def whoseTurn(self):
        """
        X goes first always, whose turn now
        :return:
        """
        nX = sum([1 for X in self.flatBoard if X == 'X'])
        nO = sum([1 for X in self.flatBoard if X == 'O'])
        if nX == nO:
            return 'X'
        else:
            return 'O'

    def executeMove(self, move):
        """
        Given a move execute it

        :param move:
        """
        if move.checkAvailiable():
            self.board[move.ind[0]][move.ind[1]] = move.chr
        else:
            raise ValueError("Invalid move attempted")

    @property
    def flatBoard(self):
        return [item for sublist in self.board for item in sublist]

    def availableSquares(self):
        """
        return a list of all available moves

        see: https://stackoverflow.com/questions/11122291/how-to-find-char-in-string-and-get-all-the-indexes
        :return:
        """
        inds1d = [i for i, ltr in enumerate(self.flatBoard) if ltr == '~']
        return self._inds1dTo2d(inds1d)

    def _inds1dTo2d(self, inds1d):
        """
        change the 1d inds to 2d
        :param inds1d:
        :return:
        """
        # can be done smarter but oh well
        indmap = {0: (0, 0),
                  1: (0, 1),
                  2: (0, 2),
                  3: (1, 0),
                  4: (1, 1),
                  5: (1, 2),
                  6: (2, 0),
                  7: (2, 1),
                  8: (2, 2)}
        out = []
        for i in inds1d:
            out.append(indmap[i])
        return out

    def isWin(self):
        """
        analyze the board for a win

        returns X or O for win, D for a draw and False if not done
        :return:
        """
        # there have to be at least 5 non '~', done as a shortcut
        if self.board.count('~') > 4:
            return False
        # check the rows
        for b in self.board:
            if ''.join(b) == 'XXX':
                return 'X'
            elif ''.join(b) == 'OOO':
                return 'O'
        # transpose and check the columns
        btmp = list(map(list, zip(*self.board)))
        for b in self.board:
            if ''.join(b) == 'XXX':
                return 'X'
            elif ''.join(b) == 'OOO':
                return 'O'
        # check the diagnol 1
        if self.board[0][0] == 'X':
            if self.board[1][1] == 'X':
                if self.board[2][2] == 'X':
                    return 'X'
        if self.board[0][0] == 'O':
            if self.board[1][1] == 'O':
                if self.board[2][2] == 'O':
                    return 'O'
        # check the diagnol 2
        if self.board[0][2] == 'X':
            if self.board[1][1] == 'X':
                if self.board[2][0] == 'X':
                    return 'X'
        if self.board[0][2] == 'O':
            if self.board[1][1] == 'O':
                if self.board[2][0] == 'O':
                    return 'O'
        # are there any '~' on the board?
        if '~' in self.flatBoard:
            return False
        else:
            return 'D'


class RandomGame(object):
    """
    play and collect a random game
    """

    def __init__(self):
        self.board = Board()
        self.moves = []
        self.winner = None

    def play(self, verbose=False):
        while self.board.isWin() is False:
            move = Move.randomMove(self.board)
            if verbose:
                print(self.board)
                print(len(self.moves), move)
            self.moves.append(move)
            self.board.executeMove(move)
        return self.board.isWin(), self.moves

    @staticmethod
    def playNow():
        RG = RandomGame()
        return RG.play()


def randomStats(ngames=10000):
    games = np.asarray([RandomGame.playNow()[0] for i in range(ngames)])
    return pd.DataFrame.from_dict({'X': [(games == 'X').sum()],
                                   'O': [(games == 'O').sum()],
                                   'D': [(games == 'D').sum()]})


def manyRandom(ngames=10000, niter=100):
    return pd.concat([randomStats(ngames) for i in range(niter)]).reset_index(drop=True)
