import os
import re
import streamlit as st
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
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

# Streamlit Configuration
st.set_page_config(page_title="Founder Finder")
st.title(" Founder Finder")

# Query Input
query = st.text_input("Ask a question about founders...")

if query:
    results = db.similarity_search(query, k=5)
    results = results[:max(3, len(results))] 
    query_tokens = tokenize(query)

    st.subheader("Top Matches")
    for r in results:
        fields = parse_content(r.page_content)

        # figure out which fields actually overlap with the query & why
        matches = []
        for fname, fval in fields.items():
            field_tokens = tokenize(fval)
            overlap = sorted(set(query_tokens) & set(field_tokens))
            if overlap:
                matches.append(f"{fname.lower()}: {', '.join(overlap)}")

        why = f"Matched on {', '.join(matches)}" if matches else "No direct field overlap"

        # display info
        st.markdown(f"**{fields.get('Name','')} — {fields.get('Role','')}**")
        st.write(f"Company: {fields.get('Company','')}")
        st.write(f"Location: {r.metadata.get('location', 'N/A')}")
        st.caption(why)

        # full details
        with st.expander("Show more"):
            st.write(f"About: {fields.get('About','')}")
            st.write(f"Idea: {fields.get('Idea','')}")
            st.write(f"Stage: {fields.get('Stage','')}")
            st.write(f"Email: {fields.get('Email','')}")
            st.write(f"Keywords: {fields.get('Keywords','')}")
            st.write(f"LinkedIn: {fields.get('LinkedIn','')}")
            st.write(f"Notes: {fields.get('Notes','')}")


        # metadata footer
        st.caption(
            f"ID: {r.metadata.get('id','N/A')}"
        )
        st.divider()


    # GPT Explanation
    context = "\n\n".join([r.page_content for r in results])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Explain why these founders match the query."},
            {"role": "user", "content": f"Query: {query}\n\n{context}"}
        ]
    )
    st.subheader("Why these matches?")
    st.write(response.choices[0].message.content)
