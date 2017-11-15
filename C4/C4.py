import itertools
import random

class Game:
    WON = 'WON'
    ERROR = 'ERROR'
    ONGOING = 'ONGOING'
    TIE = 'TIE'

    def __init__(self):
        self.board = [[None] * 6 for _ in range(7)]
        self.player = 1
        self.state = self.ONGOING

    def play(self, col):
        if self.state != self.ONGOING:
            return self.ERROR
        if col is None:
            self.player = 3 - self.player
            self.state = self.WON
            return self.state
        if not 0 <= col <= 6:
            self.state = self.ERROR
            return self.state
        for row in range(6):
            if self.board[col][row] is None:
                break
        else:
            self.state = self.ERROR
            return self.state
        self.board[col][row] = self.player

        # check accross
        for i in range(4):
            try:
                for j in range(4):
                    if self.board[col-i+j][row] != self.player:
                        break
                else:
                    self.state = self.WON
                    return self.state
            except IndexError:
                continue
        # check vertical
        if row >= 3:
            for i in range(row-3, row):
                if self.board[col][i] != self.player:
                    break
            else:
                    self.state = self.WON
                    return self.state
        # check diag up-left to down-right
        for i in range(4):
            try:
                for j in range(4):
                    if self.board[col-i+j][row+i-j] != self.player:
                        break
                else:
                    self.state = self.WON
                    return self.state
            except IndexError:
                continue
        # check diag down-left to up-right
        for i in range(4):
            try:
                for j in range(4):
                    if self.board[col-i+j][row-i+j] != self.player:
                        break
                else:
                    self.state = self.WON
                    return self.state
            except IndexError:
                continue
        # check tie
        for i in range(7):
            if self.board[i][5] is None:
                break
        else:
            self.state = self.TIE
            return self.state

        self.player = 3 - self.player
        return self.state

    def __repr__(self):
        if self.state == self.WON:
            s = f'Player {self.player} won:\n'
        elif self.state == self.ERROR:
            s = f'Got error from player {self.player}\n'
        elif self.state == self.TIE:
            s = 'Tie:\n'
        else:
            s = ''
        for i in range(5,-1,-1):
            for j in range(7):
                player = self.board[j][i]
                s += str(player) if player else ' '
            s += '\n'
        return s

    def __bool__(self):
        return self.state == Game.ONGOING

class Player:
    def reset(self, player):
        self.player = player
        self.game = Game()

    def op_move(self, move):
        self.game.play(move)

    def get_move(self):
        move = random.randint(0,6)
        while self.game.board[move][5] is not None:
            move = random.randint(0,6)
        self.game.play(move)
        return move

class SmartPlayer(Player):
    def __init__(self):
        self.mem = {}
        self.hist = []
        self.game = Game()

    def reset(self, player):
        if self.game.state == Game.WON and self.game.player == self.player:
            for board, move in self.hist:
                self.mem[board].remove(move)
        self.hist = []
        return super().reset(player)

    def get_move(self):
        board = tuple(x for l in self.game.board for x in l)
        if board not in self.mem:
            board = tuple(x for l in reversed(self.game.board) for x in l)
            if board not in self.mem:
                self.mem[board] = [x for x in range(7) if self.game.board[x][5] is None]
        choices = self.mem[board]
        if choices:
            move = random.choice(self.mem[board])
            self.hist.append((board, move))
        else:
            move = None
        self.game.play(move)
        return move

def play_game(p1, p2):
    p1.reset(1)
    p2.reset(2)
    game = Game()
    p = itertools.cycle((p1,p2)).__next__
    player = p()
    while game:
        move = player.get_move()
        game.play(move)
        #print(move)
        #print(game)
        player = p()
        player.op_move(move)
    #print(game)
    if game.state == game.WON:
        return game.player
    else:
        print(game)
        return 0


if __name__ == "__main__":
    stats = [0, 0, 0]
    p1 = Player()
    p2 = SmartPlayer()
    for i in range(1000):
        res = play_game(p1, p2)
        stats[res] += 1
        print('\r' + str(i) + ': ' + str(stats), end='')
    print()
