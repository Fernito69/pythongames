#!/usr/bin/env python
# coding: utf-8

# IMPORTS
import random
import os
import math
import time

#clears the screen
os.system("cls")

#defines the amount of players
global amount_players

print("Welcome to Fernito's Blackjack\n")

#before anything, we ask how many players will be playing

#check for errors in input
error_check = True

while error_check:            
    try:
        amount_players = int(input("How many players will be playing (1 to 4)? "))
    
    except:
        print("That's not a valid number!")
        continue 

    else:           
        if amount_players not in [1,2,3,4]:
            print("That's not a valid number!")
        else:
            error_check = False


class Deck:
    
    def __init__(self): 
        #we prepare the deck here
        
        deck_suits = ["♣","♠","♥","♦"]
        deck_numbers = ["A",2,3,4,5,6,7,8,9,"X","J","Q","K"]
        deck_prep = []
        
        for i in deck_suits:
            for j in deck_numbers:
                #1 copy of each card per player
                for k in range(amount_players):
                    deck_prep.append([i,j]) 
        
        #the deck gets shuffled!
        
        random.shuffle(deck_prep) 
                                
        self.cards = deck_prep 
    
    
    """
    PRINTS THE DECK
    """
    def print_deck(self):
        
        #number of cards left in deck
        cards_left = len(self.cards)
        
        #defines the thickness of the deck (just for aesthetic purposes)
        thiccness = math.floor((cards_left/10) + 1)

        #defines the standoff for the printing of the cards (so they're not stuck to the left side of the screen)
        standoff = " " * (9 - thiccness)

        #takes care of the standoff whether the number of cards has 1 or 2 digits
        number_standoff = "▒" * (4-len(str(cards_left)))
        
        #if there are no cards left, print an empty space!
        if cards_left < 1:
            
            deck_repr  = standoff + "╔─────╗\n"
            deck_repr += standoff + "│ \ / │\n"
            deck_repr += standoff + "│  X  │\n"
            deck_repr += standoff + "│ / \ │\n"
            deck_repr += standoff + "╚─────╝\n"
            
        else:
            #prints the deck!

            deck_repr  = standoff + "╔═════" + "╗" * thiccness + "\n"
            deck_repr += standoff + "║▒▒▒▒▒" + "║" * thiccness + "\n"
            #in the third line, we can see the number of cards left in the deck
            deck_repr += standoff + "║▒" + str(cards_left) + number_standoff +"║" * thiccness + "\n"
            deck_repr += standoff + "║▒▒▒▒▒" + "║" * thiccness + "\n"
            deck_repr += standoff + "╚═════" + "╝" * thiccness + "\n"        

        print(deck_repr)
                                        

class Entity:
    
    #AN ENTITY CAN BE EITHER THE PLAYER OR THE BANK
    
    def __init__(self):
        
        #entity attributes (shared by players and bank)
        self.hand = []
    
    
    """
    ENTITY DRAWS A CARD
    """
    def draws(self,deck):        
        
        #if deck is empty, replenishes it
        if len(deck.cards) == 0:
            deck.__init__()
            
        drawn_card = deck.cards[-1]
        deck.cards.pop()        
        self.hand.append(drawn_card)       
        
        
    """
    COUNTS THE POINTS IN THE ENTITY'S HAND
    """
    def points(self):
        
        #counts amount of aces in the player's hand
        ace_counter = 0
        for i in range(len(self.hand)):
            if self.hand[i][1] == "A":
                ace_counter += 1
        
        #proceeds to count points, but not aces!
        points = 0
        for i in range(len(self.hand)):
            if self.hand[i][1] in ["X", "J", "Q", "K"]:
                points += 10
            elif self.hand[i][1] == "A":
                pass
            else:
                points += self.hand[i][1]    
                
        #now we count the aces
        if ace_counter > 0 and (points + (10 + ace_counter)) <= 21:
            points += 10 + ace_counter
            
        else:
            points += ace_counter
        
        return points   
    

class Player(Entity):
    
    def __init__(self,player_number):
        
        #inherits class Entity
        Entity.__init__(self)
        
        #player only attributes
        
        self.name          = ""
        self.money         = 100
        self.current_bet   = 0
        self.player_number = player_number
        self.in_game       = True
        
        
    """
    ASKS FOR PLAYER'S NAME
    """
    def name_input(self):
        
        #checks for a name too long (more than 20 characters)
        error_check = True
        
        while error_check:            
            pname = input("Player " + str(self.player_number + 1) + ", what's your name? ")
                        
            if len(pname) > 20:
                print("Wow! That's a long name. Could you make it shorter?")
            else:
                error_check = False
        
        #asigns the name
        self.name = pname


    """
    PRINTS THE PLAYERS'S HAND
    """
    def print_hand(self):
        
        #defines the standoff for the printing of the cards (so they're not stuck to the left side of the screen)
        standoff    = " " * math.floor(69 / (amount_players + 1)) + " " * 13 * (self.player_number)
         
        """
        OLD STANDOFF
        standoff = " " * 13 * (self.player_number + 1)
        """
        #first determines how many cards the player has in his/her hand
        hand_count = len(self.hand)

        #if player has cards in the hand
        if hand_count > 0:

            #upper border of hand
            hand_repr = standoff + "╔═" * hand_count + "════╗\n" + standoff

            #2nd row
            for i in range(hand_count):                
                hand_repr += "║"+str(self.hand[i][1])
            hand_repr += "    ║\n" + standoff

            #3rd row
            for i in range(hand_count - 1):
                hand_repr += "║" + str(self.hand[i][0])
            hand_repr += "║  " + str(self.hand[hand_count - 1][0]) + "  ║\n" + standoff

            #4th row
            for i in range(hand_count - 1):                
                hand_repr += "║ " 
            hand_repr += "║    " + str(self.hand[hand_count - 1][1]) + "║\n" + standoff

            #lower border of hand
            hand_repr += "╚═" * hand_count + "════╝" #\n"
        
        #when player has no cards in the hand, print empty space
        else:
            hand_repr = "\n" * 4

        print(hand_repr)
   


class Bank(Entity):
    
    def __init__(self):
        
        #inherits class Entity
        Entity.__init__(self)

    """
    PRINTS THE BANK'S HAND
    """
    def print_hand(self, first_move = False):
        
        #defines the standoff for the printing of the cards (so they're not stuck to the left side of the screen)
        standoff = " " * 31
        
        #first determines how many cards the bank has in its hand
        hand_count = len(self.hand)

        #upper border of hand
        hand_repr = standoff + "╔═════╗" * hand_count + "\n" + standoff

        #the first time the bank plays, one card is face down        

        if first_move:
            #2nd row            
            for i in range(hand_count-1):
                hand_repr = hand_repr + "║"+str(self.hand[i][1])+"    ║║▒▒▒▒▒║"
            hand_repr += "\n" + standoff

            #3rd row
            for i in range(hand_count-1):
                hand_repr = hand_repr + "║  "+str(self.hand[i][0])+"  ║║▒▒▒▒▒║"
            hand_repr += "\n" + standoff

            #4th row
            for i in range(hand_count-1):                
                hand_repr = hand_repr + "║    "+str(self.hand[i][1])+"║║▒▒▒▒▒║"
            hand_repr += "\n" + standoff
        
        #Hand with all cards face up
        else:
            #2nd row
            for i in range(hand_count):                
                hand_repr = hand_repr + "║"+str(self.hand[i][1])+"    ║"
            hand_repr += "\n" + standoff

            #3rd row
            for i in range(hand_count):
                hand_repr = hand_repr + "║  "+str(self.hand[i][0])+"  ║"
            hand_repr += "\n" + standoff

            #4th row
            for i in range(hand_count):                
                hand_repr = hand_repr + "║    "+str(self.hand[i][1])+"║"
            hand_repr += "\n" + standoff

        #lower border of hand
        hand_repr += "╚═════╝" * hand_count # + "\n"

        print(hand_repr)



class Playfield():
    
    def __init__(self):
        pass
    
    
    """
    PRINTS THE PLAYFIELD
    """
    def print_playfield(self,deck,player,bank,first_move=False):
        
        #clears the screen before drawing
        os.system("cls")       
        
        print(" " * 35 + "B A N K")
        #just for debugging:
        #print(" " * 27 + "Points: " + str(bank.points()))
        bank.print_hand(first_move)
        
        
        #money on the stack
        print(" " * 36 + "STACK:") 
        
        #ATTENTION! The variable "player" is a list with every player
        stack = ""

        for i in range(amount_players):
            stack += player[i].name + ": $" + str(player[i].current_bet)
            if i < (amount_players - 1):
                stack += " / "   

        #calculates a standoff for the stack, so it's kinda centered 
        stack_standoff = math.floor((78 - len(stack))/2)

        stack = " "*stack_standoff + stack

        #prints stack
        print(stack)
        
        #prints deck
        deck.print_deck()
        
        #print("\n")

        #prints every player's hand

        for i in range(amount_players):

            #is the player still playing?
            if player[i].in_game:
                p_ingame = ""
            else:
                p_ingame = " (OUT!)"

            print(" " * math.floor(69 / (amount_players + 1)) + " " * 13 * (player[i].player_number) + player[i].name + p_ingame) 
            print(" " * math.floor(69 / (amount_players + 1)) + " " * 13 * (player[i].player_number) + "Money:  $" + str(player[i].money))
            """
            WITH OLD STANDOFF
            print(" " * 13 * (player[i].player_number + 1) + player[i].name + p_ingame) 
            print(" " * 13 * (player[i].player_number + 1) + "Money:  $" + str(player[i].money))
            #print(" " * 10 * (player[i].player_number + 1) + "Points: " + str(player[i].points()))
            """
            player[i].print_hand()
        
        #print("(q) to quit the game")
        #print("\n")
    
    """
    MAKES AN ANIMATION FOR THE FIRST MOVE OF EVERY GAME
    """
    def first_move(self,deck,player,bank):        
        
        #resets the hands of bank and players and in_game status
        for i in range(amount_players):
            player[i].hand        = []
            #player plays only if he has money
            if player[i].money > 0:
                player[i].in_game     = True
            player[i].current_bet = 0

        bank.hand = []
        
        self.print_playfield(deck,player,bank)
        
        #every player draws 2 cards
        for i in range(2):
            for j in range(amount_players):            
                if player[j].in_game:
                    player[j].draws(deck)
                    time.sleep(.5)
                self.print_playfield(deck,player,bank)
        
        #bank draws first card
        bank.draws(deck)        
        time.sleep(.5)        
        self.print_playfield(deck,player,bank)
        
        #bank draws second card
        bank.draws(deck)        
        time.sleep(.5)
        self.print_playfield(deck,player,bank,True)
        
        
    """
    PLAYER PLACES A BET
    """
    def place_bet(self,deck,player,bank):        
        
        #every player places a bet

        for i in range(amount_players):

            #check if the player has any money
            if player[i].money > 0:

                #checks for errors in input
                error_check = True
                
                while error_check:
                    
                    #checks that it's an integer
                    try:
                        p_bet = int(input(f"{player[i].name}, place your bet: "))
                    
                    except:
                        print("That's not a valid bet! Try again\n")
                        continue
                    
                    #checks that the player has enough money for the bet
                    else:
                        if p_bet > player[i].money:
                            print("You don't have that much money! Try again\n")
                            
                        else:
                            error_check = False
                
                #sets bet and re-prints playfield
                player[i].current_bet = p_bet
                player[i].money = player[i].money - p_bet
                self.print_playfield(deck,player,bank,True)
    
    
    """
    CHECK IF THE PLAYER HAS MORE THAN 21 POINTS, HE LOSES AUTOMATICALLY
    """    
    def check_player_points(self,deck,player,bank):
        
        if player.points() > 21:
            #loses the bet!
            player.current_bet = 0   
            player.in_game     = False         
            #return False
        
        else:
            pass            
            #return True  
        
        
    """
    ASKS THE PLAYER IF HE WANTS TO STAY OR DRAW ANOTHER CARD
    """
    def draw_another(self,deck,player,bank):
        
        #draw cycle for every player

        for i in range(amount_players):

            #the loop repeats itself until player decides to stays
            keep_drawing = True
            
            while player[i].in_game and keep_drawing:           
            
                #checks for errors in input
                error_check = True
                           
                while error_check:
                    stay_or_draw = input(f"{player[i].name}, would you like to stay (s), draw another card (d)? ")

                    if stay_or_draw not in ["s","d"]:
                        print("That's not a valid answer! Try again\n")
                    else:
                        error_check = False

                #draws another card, re-prints the playfield and returns True
                #if player exceeds 21 points, the cycle stops automatically
                if stay_or_draw == "d":
                    player[i].draws(deck)
                    self.check_player_points(deck,player[i],bank)
                    self.print_playfield(deck,player,bank,True)                     
                    keep_drawing = player[i].in_game
                    if not player[i].in_game:
                        input("Sorry " + player[i].name + ", you lose! Better luck next time\n")

                #stays and returns False
                elif stay_or_draw == "s":
                    self.print_playfield(deck,player,bank,True)
                    keep_drawing = False
                
                """
                elif stay_or_draw == "q":
                    self.print_playfield(deck,player,bank,True)
                    keep_drawing = False
                    return "q"
                """

        
    """
    CHECKS THE BET
    """      
    def check_bet(self,deck,player,bank):
        
        #this method runs once the bet has been placed (for every player)
               
        #we check first if the player and/or bank have a blackjack
        player_blackjack = [False] * amount_players

        for i in range(amount_players):
            player_blackjack[i] = len(player[i].hand) == 2 and player[i].points() == 21

        bank_blackjack   = len(bank.hand) == 2 and bank.points() == 21
        
        #re-prints the playfield, this time with all cards face up
        
        self.print_playfield(deck,player,bank)
        
        for i in range(amount_players):

        #checks if the bank has already more points than the players        
            if bank.points() > player[i].points() and player[i].in_game:
                #the bank wins, player loses the bet 
                player[i].current_bet = 0
                player[i].in_game = False
                self.print_playfield(deck,player,bank)                
                input("Sorry " + player[i].name + ", you lose! Better luck next time")            
                #return False
            
            #checks if it's a tie
            elif bank.points() == player[i].points() and player[i].in_game:
                player[i].money += player[i].current_bet
                player[i].current_bet = 0
                player[i].in_game = False
                self.print_playfield(deck,player,bank)
                input(player[i].name + ": it's a tie! You don't lose any money")
                #return False
            
        
        #if the bank has fewer points, must draw until it wins or loses
        bank_check = True   
        
        #if all players are out of the game, there's no bank drawing cycle
        all_players_out = 0
        for i in range(amount_players):
            if player[i].in_game:
                all_players_out += 1

        if all_players_out == 0:
            bank_check = False            

        while bank_check:
                        
            #gives it a delay, for some sort of animation feeling
            time.sleep(2)
            
            #bank draws
            """
            AQUI IF SI TIENE MÁS DE 17 PUNTOS BANK?????
            """
            bank.draws(deck)
            self.print_playfield(deck,player,bank)
            
            for i in range(amount_players):

                #checks the bank points
                if bank.points() <= 21 and player[i].in_game:
                    
                    if bank.points() > player[i].points():
                        #the bank wins, player loses the bet 
                        player[i].current_bet = 0
                        self.print_playfield(deck,player,bank)
                        player[i].in_game = False
                        input("Sorry " + player[i].name + ", you lose! Better luck next time")
                        #bank_check = False
                        #break
                        #return False
                    
                    elif bank.points() == player[i].points():
                         #it's a tie! 
                        player[i].money += player[i].current_bet
                        player[i].current_bet = 0
                        self.print_playfield(deck,player,bank)
                        player[i].in_game = False
                        input(player[i].name + ": it's a tie! You don't lose any money")
                        #bank_check = False
                        #break
                        #return False
                        
                elif bank.points() > 21 and player[i].in_game:
                    #player wins the bet!
                    if not player_blackjack[i]:
                        player[i].money += player[i].current_bet * 2
                        player[i].in_game = False                
                        input("You win, " + player[i].name + "! Congratulations")

                    #player wins and has a blackjack    
                    elif player_blackjack[i]:
                        player[i].money += player[i].current_bet * 3
                        player[i].in_game = False
                        input("BLACKJACK for " + player[i].name + "! You win the double of the amount in the stack")

                    self.print_playfield(deck,player,bank)
                    player[i].current_bet = 0

                #if all players are out of the game, breaks the cycle
                all_players_out = 0
                for i in range(amount_players):
                    if player[i].in_game:
                        all_players_out += 1

                if all_players_out == 0:
                    bank_check = False
                    #return False           



#we initialize the classes
playfield = Playfield()
deck      = Deck()
bank      = Bank()
player    = []

for i in range(amount_players):    
    player.append(Player(player_number = i))

#asks for the player's name
for i in range(amount_players):
    player[i].name_input()

#the game loop begins!
game_runs = True

while game_runs:
    
    #the turn begins!
    game_turn = True
    
    while game_turn:

        #if all players ran out of money, the game ends
        money_check = 0

        for i in range(amount_players):
            if player[i].money > 0:
                money_check += 1

        if money_check == 0:
            print("\nAll players ran out of money!")
            game_runs = False
            break              
        
        
        #makes the first move (draws 2 cards for each entity, with an animation)
        playfield.first_move(deck,player,bank)

        #player places bet
        playfield.place_bet(deck,player,bank)

        #player draw cycle
        playfield.draw_another(deck,player,bank)
                    
        #if player has more than 21 points, in_game status is false
        for i in range(amount_players):
            playfield.check_player_points(deck,player[i],bank) 
        
        #bet checking cycle
        playfield.check_bet(deck,player,bank)                
    
    
print("Thanks for playing!")
