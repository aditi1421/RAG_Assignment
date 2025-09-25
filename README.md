### Founder Finder
Built with Python, Streamlit, FAISS, LangChain, and OpenAI.

## 📂 Project Structure
```
├── dataset.py # Generates founders.csv using Faker
├── load.py # Converts dataset to LangChain docs & builds FAISS index
├── app.py # Streamlit UI for querying & explanations
├── query.py # CLI version for testing
├── founders.csv # Synthetic dataset 
├── founders_index/ # FAISS index files 
├── requirements.txt # Dependencies
└── .gitignore # Ignores .env, pycache, etc.
```
--- 
### Image of Dataset that is created using Faker 
<img width="1086" height="247" alt="Screenshot 2025-09-25 at 4 44 33 PM" src="https://github.com/user-attachments/assets/12ec8d6b-393e-48e1-af05-07cbcccdfc0b" />
