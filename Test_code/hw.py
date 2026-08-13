import os
import chromadb

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Create/load Chroma database
chroma_client = chromadb.PersistentClient(path="./chroma_db")

memories = chroma_client.get_or_create_collection(
    name="memories"
)

# Store memories
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

print("\nstored:", memories.count(), "my_facts")

# User types the question in the terminal
question = input("Ask a question: ")

# R = Retrieve
results = memories.query(
    query_texts=[question],
    n_results=2
)

notes = "\n".join(results["documents"][0])

# A = Augment
prompt = f"""
Using these notes:

{notes}

Answer the question below:

{question}
"""

print("\nPrompt sent to AI:")
print(prompt)

# G = Generate
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GITHUB_TOKEN")
)

r = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\nAI answer:")
print(r.choices[0].message.content)