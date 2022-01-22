import discord
from PIL import Image
from Player_class import Player     # importa la clase PLAYER, como agregar una lbreria pero con una clase
from discord.ext import commands

bot = commands.Bot(command_prefix='=', help_command=None)


@bot.event
async def on_ready():   # Checa si el bot esta listo para usarse
    print("sensei is online")


@bot.command()
async def jitsu(ctx, player_2: discord.Member = None): # Empieza una partida de card-jitsu
    print("jitsu command called")

    player_1 = ctx.message.author

    if player_2 == None:
        print("play the IA")    # en un futuro la idea es poder desafiar al sensei, crear una "ia" chafita
    else:
        print(f"A match between {player_1.mention} and {player_2.mention} has started") # imprime mensaje de desafio
        await ctx.send(f"{player_1.mention} challenge {player_2.mention} | type **<accept>** to jitsu")

        def check(m):
            return m.channel == ctx.channel and m.author == player_2

        response = await bot.wait_for("message", check=check)
        print(response.content)

        if response.content == "accept":    # checa por la respuesta del jugador desafiado
            players = [Player(player_1), Player(player_2)]
            players_dm = [await player_1.create_dm(), await player_2.create_dm()]
            for player in players:  # crea los masos de ambos jugadores
                player.new_deck()
            run = True
            while run:
                for player in players:  # crea la imagen del maso
                    deck_image_list = []
                    for card in player.deck:
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

                    file = discord.File("assets/deck.png", filename="deck.png") #crea el mensaje embed con la imagen del maso

                    embed = discord.Embed(title=f"{player.name} deck: ", color=0xffffff)
                    embed.set_image(url="attachment://deck.png")

                    await players_dm[players.index(player)].send(embed=embed, file=file)

                    def check(m):   # espera por la respuesta del jugador y la guarda en el atributo self.choice
                        return m.channel == players_dm[players.index(player)] and m.author == player_1

                    choice = await bot.wait_for("message", check=check)
                    player.choice = int(choice.content) - 1

                if players[0].deck[players[0].choice].element == players[1].deck[players[1].choice].element:  # determina que carta gano
                    if players[0].deck[players[0].choice].level < players[1].deck[players[1].choice].level:
                        players[1].win_conditions.append(players[1].deck[players[1].choice])
                        await ctx.send("Same element: {}\n {} < {} PLAYER 2 wins".format(players[0].deck[players[0].choice].element,
                                                                                         players[0].deck[players[0].choice].level,
                                                                                         players[1].deck[players[1].choice].level))
                    elif players[0].deck[players[0].choice].level > players[1].deck[players[1].choice].level:
                        players[0].win_conditions.append(players[0].deck[players[0].choice])
                        await ctx.send("Same element: {}\n {} > {} PLAYER 1 wins".format(players[0].deck[players[0].choice].element,
                                                                                         players[0].deck[players[0].choice].level,
                                                                                         players[1].deck[players[1].choice].level))
                    else:
                        await ctx.send("Same element: {}\n {} = {} ITS A TIE no one wins".format(players[0].deck[players[0].choice].element, players[0].deck[players[0].choice].level, players[1].deck[players[1].choice].level))
                else:
                    if (players[0].deck[players[0].choice].element == "water" and players[1].deck[players[1].choice].element == "fire") or (players[0].deck[players[0].choice].element == "fire" and players[1].deck[players[1].choice].element == "snow") or (players[0].deck[players[0].choice].element == "snow" and players[1].deck[players[1].choice].element == "water"):
                        await ctx.send("Element superiority: {} vs {}\nPLAYER 1 wins".format(players[0].deck[players[0].choice].element,players[1].deck[players[1].choice].element))
                        players[0].win_conditions.append(players[0].deck[players[0].choice])
                    else:
                        await ctx.send("Element superiority: {} vs {}\nPLAYER 2 wins".format(players[0].deck[players[0].choice].element,players[1].deck[players[1].choice].element))
                        players[1].win_conditions.append(players[1].deck[players[1].choice])

                for player in players:  # remplaza la carta utilizada por una nueva
                    player.new_deck_card(player.choice)

                for player in players:  # checa cada turno si un jugador ha cumplido las condiciones para ganar el juego
                    for card1 in player.win_conditions:
                        for card2 in player.win_conditions:
                            for card3 in player.win_conditions:
                                if player.win_conditions.index(card1) == player.win_conditions.index(card2) or player.win_conditions.index(card1) == player.win_conditions.index(card3) or player.win_conditions.index(card2) == player.win_conditions.index(card3):
                                    continue
                                elif (((card1.element != card2.element) and (card1.element != card3.element) and (card2.element != card3.element)) or ((card1.element == card2.element) and (card1.element == card3.element))) and ((card1.color != card2.color) and (card1.color != card3.color) and (card2.color != card3.color)):
                                    winner = player.name
                                    # await ctx.send(f"{card1.get_info()}\n {card2.get_info()}\n {card3.get_info()}")
                                    run = False
                                    break

            await ctx.send(f"{winner} is the winner")


@bot.command()
async def help(ctx):    # muestra el mensaje de ayuda guardado en database/custom_help.txt
    string = ''
    with open("database/custom_help.txt", "r") as help_file:
        help_list = help_file.readlines()
        for line in help_list:
            string += line

    embed = discord.Embed(title='Help', description=string, color=0xffffff)
    await ctx.send(embed=embed)


@bot.command()
async def stats(ctx):   # muestra las estadisticas del jugador
    member_stats = Player(ctx.message.author)
    stats_msg = f"Score: {member_stats.stats().score}\nMoney: {member_stats.stats().money}" #aca vamos a implementar tu funcion @zaxul

    embed = discord.Embed(title=f"{ctx.message.author.name}", description=stats_msg, color=0xffffff)
    await ctx.send(embed=embed)


@bot.command()
async def belts(ctx):   # muestra un mensaje embed con todos los rangos de cinta obtenibles
    file = discord.File("assets/belts.png", filename="belts.png")

    embed = discord.Embed(title="", desc="", color=0xffffff)
    embed.set_image(url="attachment://belts.png")
    await ctx.send(embed=embed, file=file)

@bot.command()
async def test(ctx):    # comando temporal para propositos de prueba
    print("Test command called")

bot.run('ODczMTIzODYxMTEyMTc2NjUw.YQz19g.sHdJ-Z88Bw45h3Iuj_q0ZpyFMHs')