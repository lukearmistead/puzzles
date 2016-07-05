""" Just a simple implementation of war. Ends in an error because in war, no
one really wins.
"""
from random import shuffle

class Game(object):
    def __init__(self):
        self.all_cards = [] 
        self.deck1 = []
        self.deck2 = []
        self.discard1 = []
        self.discard2 = []
        self.winner = False

    def start_game(self):
        print 'getting cards'
        suits = ['h', 's', 'c', 'd']
        for card_no in xrange(2, 15):
            for suit in suits:
                self.all_cards.append((card_no, suit))
        print 'shuffling deck'
        shuffle(self.all_cards)
        half = len(self.all_cards) / 2
        print 'dealing in two players'
        self.deck1 = self.all_cards[:half]
        self.deck2 = self.all_cards[half:]

    def check_deck_lengths(self):
        # check for victory or defeat
        if len(self.deck1) + len(self.discard1) == 0:
            print 'player 2 wins!'
            self.winner = True
            return
        elif len(self.deck2) + len(self.discard2) == 0:
            print 'player 1 wins!'
            self.winner = True 
            return
        # check for empty deck in need of reshuffling    
        if len(self.deck1) == 0:
            print 'Reshuffling player 1 deck'
            self.deck1.extend(self.discard1)
            shuffle(self.deck1)
            self.discard1 = []
        if len(self.deck2) == 0:
            print 'Reshuffling player 2 deck'
            self.deck2.extend(self.discard2)
            shuffle(self.deck2)
            self.discard2 = []

    def play_turn(self):
        self.check_deck_lengths()
        card1 = self.deck1.pop()
        print 'player 1 draws:'
        print card1
        card2 = self.deck2.pop()
        print 'player 2 draws:'
        print card2
        if card1[0] > card2[0]:
            self.discard1.extend((card1, card2))
            print 'player 1 wins and receives:' 
            print card2 
        elif card1[0] < card2[0]:
            self.discard2.extend((card1, card2))
            print 'player 2 wins and receives:' 
            print card1 
        elif card1[0] == card2[0]:
            print 'war'
            self.war(card1, card2)
        else:
            print 'error'

    def war(self, card1, card2):
        spoils =[]
        while card1[0] == card2[0]:
            spoils.extend((card1, card2))
            for count in xrange(2):
                self.check_deck_lengths()
                spoils.extend((self.deck1.pop(), self.deck2.pop()))
            self.check_deck_lengths()
            card1 = self.deck1.pop()
            print 'player 1 draws:'
            print card1
            card2 = self.deck2.pop()
            print 'player 2 draws:'
            print card2
        spoils.append(card1)
        spoils.append(card2)
        if card1[0] > card2[0]:
            self.discard1.extend(spoils)
            print 'player 1 wins and receives:' 
            print spoils 
        elif card1[0] < card2[0]:
            self.discard2.extend(spoils)
            print 'player 2 wins and receives:' 
            print spoils 
        else:
            print 'error'

    def count_decks(self):
        print
        print 'player 1 has:'
        print '%s cards' % (len(self.deck1) + len(self.discard1))
        print
        print 'player 2 has:'
        print '%s cards' % (len(self.deck2) + len(self.discard2))
        print


if __name__ == '__main__':
    game = Game()
    game.start_game()
    while not game.winner:
        game.count_decks()
        game.play_turn()
        print 'keep playing?'
        if raw_input():
            continue
