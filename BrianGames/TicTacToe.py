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
