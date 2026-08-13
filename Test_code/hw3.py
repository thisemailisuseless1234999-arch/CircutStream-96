import chromadb

client = chromadb.Client()

foods = client.get_or_create_collection(name="foods")

foods.add(
    documents=[
        "Pizza is my go-to comfort food.",
        "I really like eating sushi.",
        "Tacos are not one of my favorite dinners.",
        "I usually eat popcorn while watching movies.",
        "Mango ice cream is my favorite dessert.",
        "I like mangoes and strawberries as a snack.",
        "I enjoy eating pasta with sundried tomato pesto."
    ],
    ids=[
        "food1",
        "food2",
        "food3",
        "food4",
        "food5",
        "food6",
        "food7"
    ]
)

result = foods.query(
    query_texts=["What food do I like the most?"],
    n_results=1
)

print("n_results = 1")
print(result["documents"][0])

result = foods.query(
    query_texts=["What food do I like the most?"],
    n_results=3
)

print("\nn_results = 3")
print(result["documents"][0])

snack_result = foods.query(
    query_texts=["What snack do I usually eat?"],
    n_results=3
)

print("\nSnack query:")
print(snack_result["documents"][0])