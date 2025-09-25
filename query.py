import os
from dotenv import load_dotenv
import re
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

#Workaround to suppress OpenMP duplicate library error
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

#API Key check
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing API Key")

client = OpenAI()
embeddings = OpenAIEmbeddings()

# Load FAISS index
db = FAISS.load_local("founders_index", embeddings, allow_dangerous_deserialization=True)

#Parser that converts block of text into a dictionary 
def parse_content(page_content: str) -> dict:
    """Turn multi-line string into a dictionary"""
    parsed = {}         #Initialise empty dictionary

    for line in page_content.split("\n"):           #Split content into lines & process each
        if ":" in line:             #skip anything that doesn’t look like key: value
            key, val = line.split(":", 1)
            parsed[key.strip()] = val.strip()           #whitespace cleaning
    return parsed


# tokenizer that matches based on keywords and outputs it
def tokenize(text: str):
    return [t for t in re.findall(r"\b\w+\b", text.lower()) if len(t) > 2]

def search_and_explain(query: str, k: int = 3):
    # Give top k similar results from the database
    results = db.similarity_search(query, k=k)
    query_words = tokenize(query)

    print("\n Top Matches:\n")
    for i, r in enumerate(results, start=1):
        # turn parser content into a dict
        fields = parse_content(r.page_content)
        
        #Get common fields
        name = fields.get("Name", "")
        role = fields.get("Role", "")
        company = fields.get("Company", "")
        idea = fields.get("Idea", "")
        about = fields.get("About", "")
        keywords = fields.get("Keywords", "")
        notes = fields.get("Notes", "")
        
        matched_fields = []
        for field_name, value in fields.items():
            field_tokens = tokenize(value)
            found = sorted(set(query_words) & set(field_tokens))
            if found:
                matched_fields.append(f"{field_name.lower()}: {', '.join(found)}")

        #Pick snippet explaining the match
        if matched_fields:
            snippet = "; ".join(matched_fields)[:120] + "..."
        else:
            snippet = "no direct field match"

        row_id = r.metadata.get("id", "N/A")

        #Print the rows in a readable way
        print(f"Match {i} (row id {row_id})")
        print(f"{name} — {role}")
        print(f"Company: {company} | Location: {r.metadata.get('location', 'N/A')}")
        print(f"Snippet: {snippet}")

        
        print(" Show More")
        print(f"   Idea: {idea}")
        print(f"   About: {about}")
        print(f"   Keywords: {keywords}")
        print(f"   Notes: {notes}\n")
    

    #Give context for GPT by combining all the results
    context = "\n".join([r.page_content for r in results])
    
    #GPT model to explain why founders match the query
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Explain why these founders match the query."},
            {"role": "user", "content": f"Query: {query}\n\n{context}"}
        ]
    )

    print("GPT Explanation:\n")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    user_query = input("Enter your query: ")
    search_and_explain(user_query)
