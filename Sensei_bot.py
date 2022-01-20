import random
import discord
from PIL import Image
from discord.ext import commands


'''
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(help_command=None)
'''
client = commands.Bot(command_prefix='=', help_command=None)
client.remove_command('help')

color = {"navy_blue": 0x2C3E50, "black": 0x000000}  # diccionario de colores, es mas sencillo referir a codigos hex de esta forma,
                                                    # discord.py tiene su propio metodo pero de esta forma podemos personalizar mas

class show_deck():
    def __init__(self, player, deck):
        self.player = player
        self.deck = deck
        channel = player.create_dm()
        deck_image_list = []
        for card in deck:
            deck_image_list.append(f"assets/cards/Card-Jitsu_Cards_full_{card.card_number}.png")

        images = [Image.open(x) for x in deck_image_list]
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]

        new_im.save('assets/deck.png')


def check_win(wining_con, player):
    for card1 in wining_con:
        for card2 in wining_con:
            for card3 in wining_con:
                if wining_con.index(card1) == wining_con.index(card2) or wining_con.index(
                        card1) == wining_con.index(card3) or wining_con.index(
                    card2) == wining_con.index(card3):
                    continue
                elif (((card1.card_element != card2.card_element) and (
                        card1.card_element != card3.card_element) and (
                               card2.card_element != card3.card_element)) or (
                              (card1.card_element == card2.card_element) and (
                              card1.card_element == card3.card_element))) and (
                        (card1.card_color != card2.card_color) and (
                        card1.card_color != card3.card_color) and (
                                card2.card_color != card3.card_color)):
                    print(f"{player} Test finish")
                    print(f"{card1.get_info()}\n {card2.get_info()}\n {card3.get_info()}")
                    return False
    return True

                                                    # "#" es remplazado por "0x"para los codigos hex
@client.event
async def on_ready():                               # muestra un mensaje cuando el bot ah iniciado/conectado de manera correcta
    print('Ready status set')

@client.command()
async def help(ctx):                                # muestra un mensaje cuando "<prefix>help" es llamado
                                                    ## necesita arreglo, el comando help default no se elimino correctamente y sigue siendo enviado cuando este es llamado

    string = ''
    with open("database/custom_help.txt", "r") as help_file:    #lee el archivo *.txt y lo guarda en una <string>
        help_list = help_file.readlines()
        for line in help_list:
            string += line

    embed = discord.Embed(title='Help', description=string, color=color["black"]) # crea un objeto Embed con la informacion de <string>
    await ctx.send(embed=embed)


@client.command()
async def stats(ctx, member: discord.Member = None): # muestra un Embed de las estad'isticas del jugador


    if member is None:
        member = ctx.message.author

    def get_belt(n):    # funcion q determina la cinta de un jugador con base en su score, de esta forma solo guardamos el score y no el color de la cinta
        if n < 500:
            return "white"
        elif n < 1500:
            return "yellow"
        elif n < 3000:
            return "orange"
        elif n < 5000:
            return "green"
        elif n < 7500:
            return "blue"
        elif n < 10500:
            return "red"
        elif n < 14000:
            return "purple"
        elif n < 18000:
            return "brown"
        else:
            return "black"

    exist = False   # asumimos q el perfil del jugador no existe

    with open("database/stats.txt", "r") as stats_file: # buscamos en el archivo database/stats.txt por el miembro del servidor
                                                        ## necesita arreglo el metodo .split() permite una sintaxis mas sencilla
        stats_list = stats_file.readlines()

        for stats in stats_list:
            stat_id = 0
            stat_member = ''
            stat_score = ''
            stat_money = ''
            for char in stats:
                if char == '-':
                    stat_id += 1
                elif stat_id == 0:
                    stat_member += char
                elif stat_id == 1:
                    stat_score += char
                else:
                    stat_money += char
            if stat_member == str(member):  # si existe exist = True
                exist = True
                break

    if exist:
        await ctx.send(f"Member: {member.name}\n"   # manda las estadisticas del jugador
                       f"Score: {stat_score}\n"
                       f"Belt: {get_belt(int(stat_score))}\n"
                       f"Money: {stat_money}")
    else:
        stats_file = open("database/stats.txt", "a")
        stats_file.write(f"\n{member}-0-0")
        stats_file.close()
        await ctx.send(f"Member: {member.name}\n"
                       f"Score: 0\n"
                       f"Belt: white\n"
                       f"Money: 0")


@client.command()
async def belts(ctx):   # muestra una imagen Embed con todas las cintas posibles
    file = discord.File("assets/belts.png", filename="belts.png")

    embed = discord.Embed(title="", desc="", color=color["black"])
    embed.set_image(url="attachment://belts.png")
    await ctx.send(embed=embed, file=file)


@client.command()
async def jitsu(ctx, player_2: discord.Member = None):

    player_1 = ctx.message.author

    '''
    elif player_2 == player_1:
        await ctx.send("One shall not improve their skills by fighting himself. "
                       "Instead try looking for a worthy opponent, I will even be glad to jitsu my self")
    '''  # add before launching

    if player_2 is None:
        print("Play the IA")
    else:
        channel_player_1 = await player_1.create_dm()
        channel_player_2 = await player_2.create_dm()

        await ctx.send(f"{player_1.mention} challenge {player_2.mention} | type **<accept>** to jitsu")

        def check(m):
            return m.channel == ctx.channel and m.author == player_2

        response = await client.wait_for("message", check=check)

        print(response.content)

        if response.content == "accept":
            await ctx.send("get ready")

            class Card:
                def __init__(self, number):
                    self.card_number = number
                    with open("database/cards.txt", "r") as deck:
                        deck_content = deck.readlines()
                        for line in deck_content:
                            var_list = line.split("-")
                            card_number_aux = var_list[0]
                            card_name_aux = var_list[1]
                            card_element_aux = var_list[2]
                            card_level_aux = var_list[3]
                            card_color_aux = var_list[4]
                            if card_number_aux == str(number):
                                self.card_number = card_number_aux
                                self.card_name = card_name_aux
                                self.card_element = card_element_aux
                                self.card_level = card_level_aux
                                self.card_color = card_color_aux
                                break

                def get_info(self):
                    return f"{self.card_number} {self.card_name} {self.card_element} {self.card_level} {self.card_color}"

            deck_1 = []
            deck_2 = []
            for i in range(0, 5):
                n = random.randint(1, 25)
                deck_1.append(Card(n))
                n = random.randint(1, 25)
                deck_2.append(Card(n))

            run = True

            win_conditions_1 = []
            win_conditions_2 = []
            # card_element = {"":"", "":"", "":""}



            '''await channel.send(embed=embed, file=file)

                def check(m):
                    return m.channel == channel and m.author == player

                choice = await client.wait_for("message", check=check)

                return int(choice.content)'''

            while run:

                '''deck_image_list = []
                for card in deck_1:
                    deck_image_list.append(f"assets/cards/Card-Jitsu_Cards_full_{card.card_number}.png")

                images = [Image.open(x) for x in deck_image_list]
                widths, heights = zip(*(i.size for i in images))

                total_width = sum(widths)
                max_height = max(heights)

                new_im = Image.new('RGB', (total_width, max_height))

                x_offset = 0
                for im in images:
                    new_im.paste(im, (x_offset, 0))
                    x_offset += im.size[0]

                new_im.save("assets/deck.png")

                file = discord.File("assets/deck.png", filename="deck.png")

                embed = discord.Embed(title=f"{player_1.name} deck: ", color=color["black"])
                embed.set_image(url="attachment://deck.png")'''

                player_deck = await show_deck(player_1, deck_1)

                file = discord.File("assets/deck.png", filename="deck.png")

                embed = discord.Embed(title=f"{player_deck.player.name} deck: ")
                embed.set_image(url="attachment://belts.png")

                await channel_player_1.send(embed=embed, file=file)

                def check(m):
                    return m.channel == channel_player_1 and m.author == player_1

                choice1 = await client.wait_for("message", check=check)

                choice1 = int(choice1.content)
                choice1 = choice1 - 1
                '''
                i = 0
                embed = discord.Embed(title=f"{player_2.name} deck: ")
                for card in deck_2:
                    embed.add_field(name=f"\u200b", value=f"**{str(i + 1)})** {card.card_number} {card.card_name} {card.card_element} {card.card_level} {card.card_color}", inline=False)
                    i += 1'''

                del player_deck

                player_deck = await show_deck(player_2, deck_2)

                file = discord.File("assets/deck.png", filename="deck.png")

                embed = discord.Embed(title=f"{player_deck.player.name} deck: ")
                embed.set_image(url="attachment://belts.png")

                await channel_player_1.send(embed=embed, file=file)

                def check(m):
                    return m.channel == channel_player_2 and m.author == player_2
                choice2 = await client.wait_for("message", check=check)

                choice2 = int(choice2.content)
                choice2 = choice2 - 1

                del player_deck

                '''choice1 = show_deck(player_1, deck_1) - 1
                choice2 = show_deck(player_2, deck_2) - 1'''

                if deck_1[int(choice1)].card_element == deck_2[int(choice2)].card_element:  # logic 1/2
                    if deck_1[int(choice1)].card_level < deck_2[int(choice2)].card_level:
                        win_conditions_2.append(deck_2[int(choice2)])
                        await ctx.send("Same element: {}\n {} < {} PLAYER 2 wins".format(deck_1[int(choice1)].card_element,
                                                                                         deck_1[int(choice1)].card_level,
                                                                                         deck_2[int(choice2)].card_level))
                    elif deck_1[int(choice1)].card_level > deck_2[int(choice2)].card_level:
                        win_conditions_1.append(deck_1[int(choice1)])
                        await ctx.send("Same element: {}\n {} > {} PLAYER 1 wins".format(deck_1[int(choice1)].card_element,
                                                                                         deck_1[int(choice1)].card_level,
                                                                                         deck_2[int(choice2)].card_level))
                    else:
                        await ctx.send("Same element: {}\n {} = {} ITS A TIE no one wins".format(deck_1[int(choice1)].card_element,
                                                                                                 deck_1[int(choice1)].card_level,
                                                                                                 deck_2[int(choice2)].card_level))
                else:
                    if (deck_1[int(choice1)].card_element == "water" and deck_2[int(choice2)].card_element == "fire") or (deck_1[int(choice1)].card_element == "fire" and deck_2[
                        int(choice2)].card_element == "snow") or (deck_1[int(choice1)].card_element == "snow" and deck_2[int(choice2)].card_element == "water"):
                        await ctx.send("Element superiority: {} vs {}\nPLAYER 1 wins".format(deck_1[int(choice1)].card_element,
                                                                                             deck_2[int(choice2)].card_element))
                        win_conditions_1.append(deck_1[int(choice1)])
                    else:
                        await ctx.send("Element superiority: {} vs {}\nPLAYER 2 wins".format(deck_1[int(choice1)].card_element,
                                                                                             deck_2[int(choice2)].card_element))
                        win_conditions_2.append(deck_2[int(choice2)])

                n = random.randint(1, 25)  # append new card to the player docks
                deck_1[int(choice1)] = Card(n)
                n = random.randint(1, 25)
                deck_2[int(choice2)] = Card(n)
                                                                 # logic 2/2
                '''conditions_water = []  
                conditions_fire = []
                conditions_snow = []
                for condition in win_conditions_1:
                    if condition.card_element == "water":
                        conditions_water.append(condition)
                    elif condition.card_element == "fire":
                        conditions_fire.append(condition)
                    elif condition.card_element == "snow":
                        conditions_snow.append(condition)

                if len(conditions_water) >= 3 or len(conditions_fire) >= 3 or len(conditions_snow) >= 3 or (
                        len(conditions_water) > 0 and len(conditions_fire) > 0 and len(conditions_snow) > 0):

                    await ctx.send("PLAYER 1 WINS!")'''
                run = check_win(win_conditions_1, player_1)

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

                    if conditions_water >= 3 or conditions_fire >= 3 or conditions_snow >= 3 or (
                            conditions_water > 0 and conditions_fire > 0 and conditions_snow > 0):
                        await ctx.send("PLAYER 2 WINS!")
                        run = False
        else:
            await ctx.send("too bad")


@client.command()
async def invite(ctx):
    x = discord.utils.oauth_url(873123861112176650, permissions=None, guild=None, redirect_uri=None, scopes=None)
    await ctx.send(x)
    print("invite command succesfull")

@client.command()
async def test(ctx):
    file = discord.File("assets/deck.png", filename="deck.png")

    embed = discord.Embed(title="HI", desc="wololo", color=color["black"])
    embed.set_image(url="attachment://deck.png")
    await ctx.send(embed=embed, file=file)

    '''file = discord.File("deck.png")  # "assets/deck.png", filename=

    embed = discord.Embed(title=f"{player_1.name} deck: ")
    embed.set_image(url="attachment://deck.png")'''

client.run('ODczMTIzODYxMTEyMTc2NjUw.YQz19g.WQ3dkDGhk7Zj11KH_sfLOlgrWMw')