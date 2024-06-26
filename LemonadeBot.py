import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Lemonade Stand Game Variables
player_data = {}

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Invalid command used.')
    else:
        await ctx.send(f'An error occurred: {str(error)}')

@bot.command(name='start')
async def start_game(ctx):
    print("Start command received")  # Debugging statement
    player = ctx.author
    if player.id in player_data:
        await ctx.send(f'{player.mention} You already have a game in progress!')
    else:
        player_data[player.id] = {'money': 20, 'lemons': 0, 'sugar': 0, 'cups': 0, 'price': 1}
        await ctx.send(f'{player.mention} Welcome to your Lemonade Stand! You have $20 to start. Use !buy to purchase supplies.')

@bot.command(name='buy')
async def buy_supplies(ctx, item: str, quantity: int):
    player = ctx.author
    if player.id not in player_data:
        await ctx.send(f'{player.mention} Please start a new game with !start')
        return

    prices = {'lemons': 2, 'sugar': 1, 'cups': 0.5}
    if item not in prices:
        await ctx.send(f'{player.mention} Invalid item. You can buy lemons, sugar, or cups.')
        return

    cost = prices[item] * quantity
    if player_data[player.id]['money'] < cost:
        await ctx.send(f'{player.mention} You do not have enough money.')
    else:
        player_data[player.id]['money'] -= cost
        player_data[player.id][item] += quantity
        await ctx.send(f'{player.mention} You bought {quantity} {item} for ${cost}. You have ${player_data[player.id]["money"]} left.')

@bot.command(name='set_price')
async def set_price(ctx, price: float):
    player = ctx.author
    if player.id not in player_data:
        await ctx.send(f'{player.mention} Please start a new game with !start')
        return

    player_data[player.id]['price'] = price
    await ctx.send(f'{player.mention} You set the price of lemonade to ${price} per cup.')

@bot.command(name='sell')
async def sell_lemonade(ctx):
    player = ctx.author
    if player.id not in player_data:
        await ctx.send(f'{player.mention} Please start a new game with !start')
        return

    sales = min(player_data[player.id]['cups'], player_data[player.id]['lemons'], player_data[player.id]['sugar'])
    income = sales * player_data[player.id]['price']
    player_data[player.id]['money'] += income
    player_data[player.id]['cups'] -= sales
    player_data[player.id]['lemons'] -= sales
    player_data[player.id]['sugar'] -= sales

    await ctx.send(f'{player.mention} You sold {sales} cups of lemonade for ${income}. You now have ${player_data[player.id]["money"]}.')

@bot.command(name='status')
async def status(ctx):
    player = ctx.author
    if player.id not in player_data:
        await ctx.send(f'{player.mention} Please start a new game with !start')
        return

    status = player_data[player.id]
    await ctx.send(
        f'{player.mention} Your current status:\nMoney: ${status["money"]}\nLemons: {status["lemons"]}\nSugar: {status["sugar"]}\nCups: {status["cups"]}\nPrice per cup: ${status["price"]}'
    )

@bot.command(name='reset')
async def reset_game(ctx):
    player = ctx.author
    if player.id in player_data:
        del player_data[player.id]
        await ctx.send(f'{player.mention} Your game has been reset. You can start a new game with !start')
    else:
        await ctx.send(f'{player.mention} You do not have an active game to reset.')

# Run the bot with the token
bot.run('MTI1NTI3NTI1NjEwMTM0MzI2Mg.GVK9xg.wC9VUZyJV29CHli9P7zHG1hs_ftZ6h7a7GICmU')
