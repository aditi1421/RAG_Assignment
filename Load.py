import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain.schema import Document
import pandas as pd

load_dotenv()

# Load dataset
df = pd.read_csv("founders.csv") 

#Get API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing API key")

embeddings = OpenAIEmbeddings()

#Convert rows to document
docs = []
for _, row in df.iterrows():
    text = f"""
    Name: {row['founder_name']}
    Email: {row['email']}
    About: {row['about']}
    Role: {row['role']}
    Company: {row['company']}
    Idea: {row['idea']}  
    Stage: {row['stage']}
    Keywords: {row['keywords']}
    LinkedIn: {row['linked_in']}
    Location: {row['location']}
    Notes: {row['notes']}
    """
    docs.append(Document(
                page_content=text, 
                metadata={"id": row["id"], "stage": row["stage"], "location": row["location"]}
    ))

#Build the FAISS index
db = FAISS.from_documents(docs, embeddings)
db.save_local("founders_index")
