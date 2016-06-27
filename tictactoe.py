class ttt(object):
    def __init__(self):
        self.board = [[0,0,0],[0,0,0],[0,0,0]]
        self.active_player = 1
        self.keep_playing = True
    
    def take_turn(self):
        # check for game over
        if self.active_player == 1:
            print 'player %s select move coordinates (x, y)' % 'O'
        elif self.active_player == 10:
            print 'player %s select move coordinates (x, y)' % 'X'
        y = int(raw_input('enter x > '))
        x = int(raw_input('enter y > '))
        # check to see if spot is taken
        while self.board[x][y] > 0:
            print 'that spot is taken, please try again'
            print 'player %s, select move coordinates (x, y)' % self.active_player
            y = int(raw_input('enter x > '))
            x = int(raw_input('enter y > '))
        ### Add check to make sure coordinates are within board bounds
        self.board[x][y] += self.active_player
        
    def switch_players(self):
        if self.active_player == 1:
            self.active_player = 10
        else:
            self.active_player = 1
            
    def check_board(self):
        if 0 not in [entry for row in self.board for entry in row]:
            print 'cats game, sorry you two'
            self.keep_playing=False
            return
        for i, row in enumerate(self.board):
            col = self.board[:][i]
            if sum(row) == 30 or sum(col) == 30:
                print 'player 10 wins!'
                self.keep_playing = False
            elif sum(row) == 3 or sum(col) == 3:
                print 'player 1 wins!'
                self.keep_playing = False
        diagonal = [self.board[i][i] for i in xrange(3)]
        other_diagonal = [self.board[i][2 - i] for i in xrange(3)]
        if sum(diagonal) == 30 or sum(other_diagonal) == 30:
            print 'player 10 wins!'
            self.keep_playing = False
        elif sum(diagonal) == 3 or sum(other_diagonal) == 3:
            print 'player 1 wins!'
            self.keep_playing = False

    def display_board(self):
        mask = {10: 'X', 1: 'O', 0: '.'}
        for row in self.board:
            print ' '.join([mask[entry] for entry in row])

def main():
    game = ttt()
    print 'lets play tic tac toe!'
    while game.keep_playing:
        game.display_board()
        game.check_board()
        if not game.keep_playing:
            break
        game.take_turn()
        game.switch_players()
    
        
if __name__ == '__main__':
    main()
