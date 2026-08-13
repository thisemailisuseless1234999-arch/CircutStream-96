import discord
from discord.ext import commands
import random
from openai import OpenAI
import pandas as pd
import surprise
from surprise import Reader, Dataset, SVD, accuracy
import json

TOKEN = "MTUzMzkxNDAxMjc1MDcwODc3Ng.GIh27H.HqkUZOJxoJI21KrN06mp06Sbklc8iZF8BTy3Do"

client = OpenAI(api_key="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")

ratings_df = pd.read_csv("ratings.csv")
movie_df = pd.read_csv("movies.csv")

movie_system_instructions = """
You are acting as a middle-man interface between a Discord user
and a backend movie recommendation system.

You may only mention movies, movie IDs, genres, ratings, and recommendations
that are explicitly returned by the provided tools.

Do not invent movie titles, ratings, genres, IDs, or any other movie information.

If a movie is not returned by the search_movie tool, say:
"That movie was not found in the dataset."

If recommending movies, only recommend movies returned by get_top_movies.
Always include the estimated rating returned by the tool.

If a user asks about something unrelated to rating, searching, or movie
recommendations, say:
"I can only provide assistance finding out information about movie recommendations"""

reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings_df[["userId", "movieId", "rating"]], reader)
trainset = data.build_full_trainset()
algo = SVD(n_factors=82, n_epochs=120, lr_all=0.02, random_state=123)
algo.fit(trainset)

tools = [
    {
        "type": "function",
        "name": "get_top_movies",
        "description": "Recommend top movies for the user. The user is inferred from the Discord context.",
        "parameters": {
            "type": "object",
            "properties": {
                "num_movies": {
                    "type": "integer",
                    "description": "Number of movies to recommend",
                    "default": 5
                }
            },
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "search_movie",
        "description": "Search for movies that contain a given string in their title.",
        "parameters": {
            "type": "object",
            "properties": {
                "partial_movie_name": {
                    "type": "string",
                    "description": "A part of the movie name to search for"
                }
            },
            "required": ["partial_movie_name"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "rate",
        "description": "Add a rating entry to the ratings dataset.",
        "parameters": {
            "type": "object",
            "properties": {
                "movieId": {
                    "type": "string",
                    "description": "Movie ID to rate"
                },
                "rating": {
                    "type": "number",
                    "description": "Rating between 0.5 and 5.0"
                }
            },
            "required": ["movieId", "rating"],
            "additionalProperties": False
        }
    }
]

def get_top_movies(userid, num_movies=5):
    rated_movieIds = ratings_df[ratings_df["userId"] == userid]["movieId"].values
    unrated_movies = movie_df[~movie_df["movieId"].isin(rated_movieIds)]

    predicted_ratings = []

    for movie_id in unrated_movies["movieId"]:
        prediction = algo.predict(userid, movie_id)
        predicted_ratings.append(prediction.est)

    recommendations_df = pd.DataFrame({
        "title": unrated_movies["title"],
        "predicted_rating": predicted_ratings
    }).sort_values("predicted_rating", ascending=False)

    top_recommendations = recommendations_df.head(num_movies)

    return top_recommendations

def search_movie(partial_movie_name):
    search_results = movie_df[movie_df["title"].str.contains(partial_movie_name)][["movieId", "title", "genres"]]

    if len(search_results) > 0:
        return search_results
    else:
        return None
    pass

def rate(userid, movieId, rating):
    global ratings_df

    rating = float(rating)

    if 5 >= rating >= 0.5:
        new_row = pd.DataFrame({
            "userId": [userid],
            "movieId": [movieId],
            "rating": [rating],
            "timestamp": [0]
        })

        ratings_df = pd.concat([ratings_df, new_row], ignore_index=True)
        ratings_df.to_csv("ratings.csv", index=False)

        return "rating has been saved"
    else:
        return "rating is out of range"
    pass

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!',intents=intents)
last_response_ids = {}

@bot.event
async def on_ready():
  print(f"{bot.user} is ready!!")

@bot.command(help="Ask AI a question!")
async def ask(context, *, user_choice):

    if context.author.id in last_response_ids:
        response = client.responses.create(
            model="gpt-5-nano",
            instructions=movie_system_instructions,
            tools=tools,
            previous_response_id=last_response_ids[context.author.id],
            input=user_choice
        )
    else:
        response = client.responses.create(
            model="gpt-5-nano",
            instructions=movie_system_instructions,
            tools=tools,
            input=user_choice
        )

    tool_calls = [item for item in response.output if item.type == "function_call"]

    while tool_calls:
        tool_outputs = []

        for tool_call in tool_calls:
            function_name = tool_call.name

            if isinstance(tool_call.arguments, str):
                arguments = json.loads(tool_call.arguments)
            else:
                arguments = tool_call.arguments

            if function_name == "get_top_movies":
                output = get_top_movies(context.author.id, **arguments)

            elif function_name == "search_movie":
                output = search_movie(**arguments)

                if output is not None:
                    output = output.to_string(index=False)
                else:
                    output = "No matches"

            elif function_name == "rate":
                output = rate(context.author.id, **arguments)

            else:
                output = f"Unknown function {function_name}"

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(output)
            })

        response = client.responses.create(
            model="gpt-5-nano",
            tools=tools,
            previous_response_id=response.id,
            input=tool_outputs
        )

        tool_calls = [item for item in response.output if item.type == "function_call"]

    last_response_ids[context.author.id] = response.id

    await context.send(response.output_text)

bot.run(TOKEN)