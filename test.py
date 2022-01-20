import random


class Card:
    def __init__(self, number):
        self.card_number = number
        with open("database/cards.txt", "r") as deck:
            deck_content = deck.readlines()
            for line in deck_content:
                aux = 0
                card_number_aux = ''
                card_name_aux = ''
                card_element_aux = ''
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
                        card_element_aux += char
                    elif aux == 3:
                        card_level_aux += char
                    elif aux == 4:
                        card_color_aux += char
                if card_number_aux == str(number):
                    self.card_number = card_number_aux
                    self.card_name = card_name_aux
                    self.card_element = card_element_aux
                    self.card_level = card_level_aux
                    self.card_color = card_color_aux
                    break

    def get_info(self):
        return f"{self.card_number} {self.card_name} {self.card_element} {self.card_level} { self.card_color}"


def check_win(wining_con, player):
    for card1 in wining_con:
        for card2 in wining_con:
            for card3 in wining_con:
                if wining_con.index(card1) == wining_con.index(card2) or wining_con.index(card1) == wining_con.index(card3) or wining_con.index(card2) == wining_con.index(card3):
                    continue

                #3 dif dif
                #3 mis dif

                elif (((card1.card_element != card2.card_element) and (card1.card_element != card3.card_element) and (card2.card_element != card3.card_element)) or ((card1.card_element == card2.card_element) and (card1.card_element == card3.card_element))) and ((card1.card_color != card2.card_color) and (card1.card_color != card3.card_color) and (card2.card_color != card3.card_color)):
                    print(f"{player} Test finish")
                    print(f"{card1.get_info()}\n {card2.get_info()}\n {card3.get_info()}")
                    return False
    return True


run = True
wining_con1 = []

while run:
    n = random.randint(1, 25)
    new_card = Card(n)
    wining_con1.append(new_card)
    print(new_card.get_info())
    run = check_win(wining_con1, "wissens")