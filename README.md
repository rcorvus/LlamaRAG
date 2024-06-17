# Llama3 RAG
RAG (Retrieval Augmented Generation) Q&A API that allows text and PDF files to be uploaded via api and persisted to a vector store then queried with natural language questions.  Sources are returned along with the answer in json format. Previously uploaded documents are overwritten when a document with the same filename is uploaded again. Note: Since there's no way to know if the chunks of the new document will align with the old document (even if there are the same number of chunks because the information could have been rearranged), this solution simply deletes all the chunks of the old document before uploading the chunks of the new document.

Created with Python, Llama3, LangChain, Ollama and ChromaDB in a Flask API based solution.

## How to use
### Use Postman to test your api, you can download it here:  https://www.postman.com/downloads
1. Create a folder called 'db' in your main app folder.  
2. Open Postman and import the json collection in the `postman` folder.
3. Run your app.py.   
4. Use the `pdf` and `txt` posts in Postman to upload your documents into the vector store.  
5. Query the vector store with the `ask_vector_store` post.

## Example queries
### What does a protocol droid look like?
   ![image](https://github.com/rcorvus/LlamaRAG/assets/5025458/80526c04-c370-44a4-8b2f-ed1830d23fe7)  

### What are astromech droids called?
   ![image](https://github.com/rcorvus/LlamaRAG/assets/5025458/0de91f6a-40d3-4127-b445-7acf03d98470)

## How to install Ollama

1. Download Ollama from [here](https://ollama.com/download) (it works on Linux, Mac, and Windows)  
2. Install it.
3. In Powershell/cmd, run ```ollama pull llama3```, which pulls the "small" 8B LLM, or ```ollama pull llama3:70b``` to pull the giant 70B LLM.  The 8b downloads pretty quickly but the 70b took several hours because it's 40GB and the connection kept crashing requiring me to keep restarting the pull.
4. Start the ollama service on your computer by running ```ollama serve```
5.  Verify the ollama service is running on your computer.  Here it is running on my laptop in systray:  
![image](https://github.com/rcorvus/R2D2OpenAILlama3/assets/5025458/6e5e3906-86eb-42b0-b450-4cb8dbb8a2e7)

