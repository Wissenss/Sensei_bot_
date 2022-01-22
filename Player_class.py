import random

with open("database/cards.txt", "r") as all_cards:
    cards_amount = len(all_cards.readlines())


class Card: # clase CARTA, cada objeto de la clase tiene atributos: numero, nombre, elemento, nivel y color
    def __init__(self, number):
        self.card_number = number
        with open("database/cards.txt", "r") as deck:   # itera por el archivo de cartas y determina los atributos si el numero de carta coincide con el proporcionado al crear el objeto
            deck_content = deck.readlines()
            for line in deck_content:
                var_list = line.split("-")
                self.number = var_list[0]
                self.name = var_list[1]
                self.element = var_list[2]
                self.level = var_list[3]
                self.color = var_list[4]
                if self.number == str(number):
                    break

    def get_info(self): # regresa una string con todos los atributos de la carta
        return f"{self.number} {self.name} {self.element} {self.level} {self.color}"


class Stats:    # clase ESTADISTICAS, cada objeto tiene atributos: usuario, puntaje y dinero
    def __init__(self, user):
        self.exist = False
        with open("database/stats.txt", "r") as stats_file: # lo mismo q hace en CARTA pero con el archivo correspondiente a ESTADISTICAS para determinar los valores de sus atributos
            stats_all = stats_file.readlines()
            for stats_one in stats_all:
                stats_list = stats_one.split(',')
                self.user = stats_list[0]
                self.score = stats_list[1]
                self.money = stats_list[2]
                if self.user == user:
                    self.exist = True
                    break

    def new_entry(self, user):  # crea una nueva entrada en el archivo con los valores por defecto
        with open("database/stats.txt", "a") as stats_file:
            stats_file.write(f"\n{user},0,0")


class Player:
    def __init__(self, name): # constructor de la clase, inicializa sus atributos: nombre, eleccion, condiciones de victoria y maso
        self.name = name
        self.choice = 0
        self.win_conditions = []
        self.deck = []

    def card(self, number): # crea una instancia/objeto de la clase CARTA mediante esta clase
        return Card(number)

    def stats(self):    # crea una instancia de la clase ESTADISTICAS mediante esta clase, si el nombre del jugador no se encuantra en el archivo llama al metodo new_entry
        stats = Stats(self.name)
        if stats.exist == True:
            return stats
        elif stats.exist == False:
            stats.new_entry(self.name)
            return stats

    def new_deck(self): # crea un arreglo de 5 cartas al azar, este es el maso
        for i in range (5):
            self.deck.append(Card(random.randint(1, cards_amount)))

    def new_deck_card(self, index): # remplaza una carta del maso
        self.deck[index] = Card(random.randint(1, cards_amount))

