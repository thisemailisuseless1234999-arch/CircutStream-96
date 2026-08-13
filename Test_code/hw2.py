import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

friends_movies = {
  "Friends":["Tom", "Angela", "Leighton", "Kylan", "Amelie", "Franklin", "Marceline", "Jayden", "Saoirse", "Dilan", "Jolene", "Antonio", "Keily", "Lucian", "Scarlett", "Maxton", "Jordan", "Flynn", "Carolina", "Kase", "Marina", "Bryant"],
  "Movies":["Inception", "Avatar", "Gladiator", "Titanic", "Jaws", "Goodfellas", "Casablanca", "Psycho", "Memento", "Platoon", "Whiplash", "Amadeus", "Unforgiven", "Braveheart", "Goodwill", "Rocky", "Hamilton", "Speed", "Zodiac", "Arrival", "Vertigo", "Halloween"]
}

load_dotenv()
MY_TOKEN = os.getenv("MY_TOKEN")

@bot.event
async def on_ready():
  print(f'{bot.user} is now online!')


@bot.command(name="search")
async def search(ctx, user_choice):
    user_choice = user_choice.capitalize()

    try:
        person_index = friends_movies["Friends"].index(user_choice)
    except ValueError:
       await ctx.send(f"That person has not rated any movie. Please choose someone from this list: {friends_movies["Friends"]}")
       return

    movie = friends_movies["Movies"][person_index]

    await ctx.send(f"You have chosen {user_choice}. {user_choice} highly recommends the movie {movie}")



bot.run(MY_TOKEN)
       

    