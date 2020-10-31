
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True


class Card:
    
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
    
    def __str__(self):
        return (f'{self.rank} of {self.suit}')


class Deck: #collection of 52 cards
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deck_cards = ''
        for card in self.deck:
            deck_cards += '\n' + card.__str__()
        return 'The deck has:' + deck_cards
            
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()


test_deck = Deck()
test_deck.shuffle()

class Chips:
    
    def __init__(self,total=100):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet



class Hand: #represents computer or player
    def __init__(self,totalchips):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value, total value at any point in the hand
        self.aces = 0 
        self.totalchips = totalchips # add an attribute to keep track of aces
    
    def add_card(self,card): #This is a card resulted from a deal in Deck class
        self.cards.append(card)
        self.value+= values[card.rank] #if values is >21 whoever has this hand, has lost
        
        #check for aces
        if card.rank== 'Ace':
            self.aces +=1
    
    def adjust_for_ace(self):
        #if value > 21 make ace 1 if I still have an ace
        while self.value >=21 and self.aces:  #treating number as boolean if aces>0, its true
            self.aces -= 1
            self.value -= 10 #value is 1
            
        

test_deck = Deck()
test_deck.shuffle()

player_chips = Chips() #changing default chips to 50
player_hand = Hand(player_chips.total)



pooled_card = test_deck.deal()
print(pooled_card)
player_hand.add_card(pooled_card)
print(player_hand.cards[0])


print(player_hand.cards[0])
player_hand.aces


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips you want to bet?'))
        except:
            print('Please provide an integer.')
        else:
            if chips.bet>chips.total:
                print(f'You don\'t have enough chips. You have {chips.total}')
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        choice = input('Do you want to hit(Type in h) or stand(Type in s)? ')
        
        if choice == 'h':
            hit(deck,hand)
        elif choice == 's':
            print("Player stands. Dealer is playing.")
            playing = False
        else:
            print('Please type h or s!')
        break


def show_some(player,dealer):
   print("\nDealer's Hand:")
   print("---------------")
   print(" <<<card hidden>>>")
   print('',dealer.cards[1])  
   print("\nPlayer's Hand:\n---------------", *player.cards, sep='\n ')
   
def show_all(player,dealer):
   print("\nDealer's Hand:\n---------------", *dealer.cards, sep='\n ')
   print("---------------")
   print("Dealer's Hand =",dealer.value)
   print("\nPlayer's Hand:\n---------------", *player.cards, sep='\n ')
   print("Player's Hand =",player.value)


def player_busts(player,dealer,chips):
    print('\n')
    print('******BUST PLAYER******')
    chips.lose_bet()
    player.totalchips = chips.total

def player_wins(player,dealer,chips):
    print('\n')
    print(':) PLAYER WINS :)')
    chips.win_bet()
    player.totalchips = chips.total


def dealer_busts(player,dealer,chips):
    print('\n')
    print('*BUST DEALER* PLAYER WINS!!!! ')
    chips.win_bet()
    player.totalchips = chips.total

def dealer_wins(player,dealer,chips):
    print('\n')
    print('******DEALER WINS******')
    chips.lose_bet()
    player.totalchips = chips.total

    
def push():
    print('\n')
    print('Dealer and player tie :-\ PUSH!')


player_chips = 0

while True:
    # Print an opening statement
    print('~~ Welcome to BlackJack by Shiwani ~~')
    print('Rules:\n1.Get as close to 21 as you can without going over!')
    print('2.Dealer hits until she reaches 17. \n3.Aces count as 1 or 11.')


    # Set up the Player's chips
    if player_chips == 0:
        player_chips = Chips() #changing default chips to 50
    else:
        player_chips = Chips(player_hand.totalchips)

    # Create & shuffle the deck, deal two cards to each player
    game_deck = Deck()
    game_deck.shuffle()

    player_hand = Hand(player_chips.total)
    player_hand.add_card(game_deck.deal())
    player_hand.add_card(game_deck.deal())

    dealer_hand = Hand(player_chips.total)
    dealer_hand.add_card(game_deck.deal())
    dealer_hand.add_card(game_deck.deal()) 



    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)



    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(game_deck,player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)


        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)

        break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(game_deck,dealer_hand)    

        # Show all cards
        show_all(player_hand,dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push()


    # Inform Player of their chips total 
    print("\nPlayer's winnings stand at ---> ",player_chips.total)
    
    if player_chips.total == 0 :
        print("\nPlayer's chips exhausted")
        print("Thanks for playing!")
        break

    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")

    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break
