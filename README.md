# Llama3 RAG
RAG (Retreival Augmented Generation) Q&A API that allows text and PDF files to be uploaded via api and persisted to a vector store then queried with natural language questions.  Sources are returned along with the answer in json format.

Created with Python, Llama3, LangChain, Ollama and ChromaDB in a Flask API based solution.

## How to use
### Use Postman to test your api, you can download it here:  https://www.postman.com/downloads
1. Create a folder called 'db' in your main app folder.  
2. Open Postman and import the json collection in the `postman` folder.
3. Run your app.py.   
4. Use the `pdf` and `txt` posts in Postman to upload your documents into the vector store.  
5. Query the vector store with the `ask_vector_store` post.

## Example queries
   What does a protocol droid look like?
   ![image](https://github.com/rcorvus/LlamaRAG/assets/5025458/80526c04-c370-44a4-8b2f-ed1830d23fe7)  

   What are astromech droids called?
   ![image](https://github.com/rcorvus/LlamaRAG/assets/5025458/0de91f6a-40d3-4127-b445-7acf03d98470)
