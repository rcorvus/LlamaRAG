# Llama3 RAG
RAG (Retreival Augmented Generation) Q&A API that allows text and PDF files to be uploaded to a vector store and queried with natural language questions.  

Created with Python, Llama3, LangChain, Ollama and ChromaDB in a Flask API based solution.

## How to use
### Use Postman to test your api, you can download it here:  https://www.postman.com/downloads
1. Create a folder called 'db' in your main app folder.  
2. Open Postman and import the json collection in the `postman` folder.
3. Run your app.py.   
4. Use the `pdf` and `txt` posts in Postman to upload your documents into the vector store.  
5. Query the vector store with the `ask_vector_store` post.  
