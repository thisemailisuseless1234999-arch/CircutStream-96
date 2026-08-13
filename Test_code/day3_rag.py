import os
import chromadb

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://api.groq.com/openai/v1"
)

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

memories = chroma_client.get_or_create_collection(
    name="memories"
)

memories.upsert(
    documents=[
        "I do martial arts on Tuesdays.",
        "My favourite subject is chemistry.",
        "I have a cat called Biscuit."
    ],
    ids=[
        "fact1",
        "fact2",
        "fact3"
    ]
)

question = input("Ask a question: ")

results = memories.query(
    query_texts=[question],
    n_results=3
)

closest_memories = results["documents"][0]


bigger_prompt = f"""
Here are some memories about the user:

{closest_memories}

Question:
{question}

Use the memories above to answer the question.
"""

# G = Generate
r = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": bigger_prompt
        }
    ]
)

print(r.choices[0].message.content)