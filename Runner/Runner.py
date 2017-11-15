import requests

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
            return ERROR
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

    def to_dict(self):
        return {'board':self.board, 'player':self.player}


def play_game(url1, url2):
    game = Game()
    urls = (url1 + "/play", url2 + "/play")
    sess = (requests.session(), requests.session())
    while game:
        with sess[game.player-1].post(urls[game.player-1], json=game.to_dict()) as r:
            move = int(r.text) - 1
        game.play(move)
    #print(game)
    if game.state == game.WON:
        sess[0].get(url1 + "/win", params={'win':int(game.player==1)})
        sess[1].get(url2 + "/win", params={'win':int(game.player==2)})
        return game.player
    else:
       return 0


if __name__ == "__main__":
    stats = [0, 0, 0]
    for i in range(1000):
        res = play_game('http://127.0.0.1:5555', 'http://127.0.0.1:5555')
        stats[res] += 1
        print('\r' + str(i) + ': ' + str(stats), end='')
    print()
