import random

#maybe inherit the class card from a dock class and include the deck no longer as a list, but as a class method
class Card:
    def __init__(self, number):
        self.card_number = number
        with open("database/cards.txt", "r") as deck:
            deck_content = deck.readlines()
            for line in deck_content:
                aux = 0
                card_number_aux = ''
                card_name_aux = ''
                card_level_aux = ''
                card_color_aux = ''
                for char in line:
                    if char == '-':
                        aux += 1
                    elif aux == 0:
                        card_number_aux += char
                    elif aux == 1:
                        card_name_aux += char
                    elif aux == 2:
                        card_color_aux += char
                    elif aux == 3:
                        card_level_aux += char
                if card_number_aux == str(number):
                    self.card_number = card_number_aux
                    self.card_name = card_name_aux
                    self.card_color = card_color_aux
                    self.card_level = card_level_aux
                    break


deck_1 = []
deck_2 = []
for i in range(0, 5):
    n = random.randint(21, 70)
    deck_1.append(Card(n))
    n = random.randint(21, 70)
    deck_2.append(Card(n))

run = True

win_conditions_1 = []
win_conditions_2 = []

#card_element = {"":"", "":"", "":""}

while run:
    print("Player 1 deck:")
    i = 0
    for card in deck_1:
        print(str(i+1), ")", card.card_number, card.card_name, card.card_color, card.card_level)
        i += 1
    choice1 = int(input("Choose your card")) #needless to say this also runs for player 2, maybe do so on a function?
    i = 0
    for card in deck_2:
        print(str(i+1), ")", card.card_number, card.card_name, card.card_color, card.card_level)
        i += 1
    choice2 = int(input("Choose your card"))

    choice1 = choice1 - 1
    choice2 = choice2 - 1

    if deck_1[int(choice1)].card_color == deck_2[int(choice2)].card_color:                          #logic 1/2
        if deck_1[int(choice1)].card_level < deck_2[int(choice2)].card_level:
            win_conditions_2.append(deck_2[int(choice2)].card_color)
            print("Same element: {}\n {} < {} PLAYER 2 wins".format(deck_1[int(choice1)].card_color,
                                                                    deck_1[int(choice1)].card_level,
                                                                    deck_2[int(choice2)].card_level))
        elif deck_1[int(choice1)].card_level > deck_2[int(choice2)].card_level:
            win_conditions_1.append(deck_1[int(choice1)].card_color)
            print("Same element: {}\n {} > {} PLAYER 1 wins".format(deck_1[int(choice1)].card_color,
                                                                    deck_1[int(choice1)].card_level,
                                                                    deck_2[int(choice2)].card_level))
        else:
            print("Same element: {}\n {} = {} ITS A TIE no one wins".format(deck_1[int(choice1)].card_color,
                                                                            deck_1[int(choice1)].card_level,
                                                                            deck_2[int(choice2)].card_level))
    else:
        if (deck_1[int(choice1)].card_color == "agua" and deck_2[int(choice2)].card_color == "fuego") or (deck_1[int(choice1)].card_color == "fuego" and deck_2[int(choice2)].card_color == "nieve") or (deck_1[int(choice1)].card_color == "nieve" and deck_2[int(choice2)].card_color == "agua"):
            print("Element superiority: {} vs {}\nPLAYER 1 wins".format(deck_1[int(choice1)].card_color,
                                                                        deck_2[int(choice2)].card_color))
            win_conditions_1.append(deck_1[int(choice1)].card_color)
        else:
            print("Element superiority: {} vs {}\nPLAYER 2 wins".format(deck_1[int(choice1)].card_color,
                                                                        deck_2[int(choice2)].card_color))
            win_conditions_2.append(deck_1[int(choice2)].card_color)

    n = random.randint(21, 70)           #append new card to the player docks
    deck_1[int(choice1)] = Card(n)
    n = random.randint(21, 70)
    deck_2[int(choice2)] = Card(n)

    conditions_water = 0                        #logic 2/2
    conditions_fire = 0
    conditions_snow = 0
    for condition in win_conditions_1:
        if condition == "agua":
            conditions_water += 1
        elif condition == "fuego":
            conditions_fire += 1
        elif condition == "nieve":
            conditions_snow += 1

    if conditions_water >= 3 or conditions_fire >= 3 or conditions_snow >= 3 or (conditions_water > 0 and conditions_fire > 0 and conditions_snow > 0):
        print("PLAYER 1 WINS!")
        run = False

    conditions_water = 0
    conditions_fire = 0
    conditions_snow = 0
    if run:
        for condition in win_conditions_2:
            if condition == "agua":
                conditions_water += 1
            elif condition == "fuego":
                conditions_fire += 1
            elif condition == "nieve":
                conditions_snow += 1

        if conditions_water >= 3 or conditions_fire >= 3 or conditions_snow >= 3 or (conditions_water > 0 and conditions_fire > 0 and conditions_snow > 0):
            print("PLAYER 2 WINS!")
            run = False



