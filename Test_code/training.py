import surprise
from surprise import Reader, Dataset, SVD, accuracy
from surprise.model_selection import train_test_split
from surprise import accuracy
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

TOKEN = "MTUzMzkxNDAxMjc1MDcwODc3Ng.GIh27H.HqkUZOJxoJI21KrN06mp06Sbklc8iZF8BTy3Do"

bot = commands.Bot(command_prefix="!", intents=intents)

ratings_df = pd.read_csv('ratings.csv')
movie_df = pd.read_csv('movies.csv')
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings_df[["userId", "movieId", "rating"]], reader)


trainset = data.build_full_trainset()
algo = SVD(n_factors=82, n_epochs=120, lr_all=0.02)
algo.fit(trainset)

def get_rating(item):
    return item[1]

@bot.event
async def on_ready():
   print("Im Ready!!")

@bot.command(name="recommend")
async def recommend(ctx, n):
  try:
    n = int(n)
    if n <= 0:
      await ctx.send("Invalid input. Please enter a number higher than 0.")
      return
  except ValueError:
    await ctx.send("Invalid input. Please enter a valid number.")
    return

  rated_movieIds = ratings_df[ratings_df["userId"] == 1]["movieId"]
  unrated_movies = movie_df[~movie_df["movieId"].isin(rated_movieIds)]

  recommendations = []

  for index, row in unrated_movies.iterrows():
    movie_id = row["movieId"]
    movie_title = row["title"]

    prediction = algo.predict(1, movie_id)

    recommendations.append((movie_title, prediction.est))

  recommendations.sort(key=get_rating, reverse=True)

  top_recommendations = recommendations[:n]
  message = f"Top {n} recommendations:\n\n"

  for title, predicted_rating in top_recommendations:
    message += f"{title}'s predicted rating is: {predicted_rating:.2f}\n"

  await ctx.send(message)

bot.run(TOKEN)