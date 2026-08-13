import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


MY_TOKEN = "MTUzMzkxNDAxMjc1MDcwODc3Ng.GIh27H.HqkUZOJxoJI21KrN06mp06Sbklc8iZF8BTy3Do"

@bot.event
async def on_ready():
  print(f'{bot.user} is now online!')



@bot.command(name='cf')
async def cf(ctx, user_choice):
    user_choice = user_choice.capitalize()
    await ctx.send(f"You have chosen {user_choice}")
    choices = ["Heads", "Tails"]
    botcf = random.choice(choices)

    if user_choice not in choices:
       await ctx.send("Not a valid side. (heads/tails)")
       return
    elif user_choice == botcf:
        await ctx.send(f"You won! You guessed {user_choice} correctly!")
    elif user_choice != botcf:
        await ctx.send(f"I flipped the coin and got {botcf}")
        await ctx.send("Aw, you guessed wrong... Try again!")
    else:
        await ctx.send(f"I flipped the coin and got {botcf}")



bot.run(MY_TOKEN)