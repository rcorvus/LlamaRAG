from flask import Flask, request
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

folder_path = "db"

cached_llm = Ollama(model="llama3")

embedding = OpenAIEmbeddings()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

## Get result and cite sources
def process_llm_response(llm_response):
    result = llm_response['result']
    print(result)
    sources = []
    print('\n\nSources:')
    for source_doc in llm_response["source_documents"]:
        source = source_doc.metadata['source']
        print(source)
        sources.append(
            {"source": source}
        )

    return {"answer": result, "sources": sources}

@app.route("/", methods=["GET"])
def home():
    return "hello world"

@app.route("/query", methods=["POST"])
def queryPost():
    print("Post /query called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    response = cached_llm.invoke(query)

    print(response)

    response_answer = {"answer": response}
    return response_answer

@app.route("/ask_vector_store", methods=["POST"])
def ask_vector_storePost():
    print("Post /ask_vector_store called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    print("Loading vector store")

    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            # k is number of documents to return
            "k": 2,
            "score_threshold": 0.2,
        },
    )

    qa_chain = RetrievalQA.from_chain_type(llm=cached_llm, 
                                  chain_type="stuff", 
                                  retriever=retriever, 
                                  return_source_documents=True)
    
    llm_response = qa_chain.invoke(query)

    response_answer = process_llm_response(llm_response)

    return response_answer

@app.route("/txt", methods=["POST"])
def textPost():
    file = request.files["file"]
    file_name = file.filename
    save_file = "text/" + file_name
    file.save(save_file)
    print(f"filename: {file_name}")

    loader = loader = TextLoader(save_file)
    docs = loader.load_and_split()
    print(f"docs len={len(docs)}")

    chunks = text_splitter.split_documents(docs)
    print(f"chunks len={len(chunks)}")

    number_of_documents_deleted = deleteIfFoundByFilename(save_file)
    if number_of_documents_deleted > 0:
        print(f"Deleted existing {save_file}: {number_of_documents_deleted} chunks deleted from vector store")

    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path
    )
    vector_store.persist()

    print(f"Successfully Uploaded {file_name}")
    response = {
        "status": "Successfully Uploaded",
        "filename": file_name,
        "doc_len": len(docs),
        "chunks": len(chunks),
    }
    return response

@app.route("/pdf", methods=["POST"])
def pdfPost():
    file = request.files["file"]
    file_name = file.filename
    save_file = "pdf/" + file_name
    file.save(save_file)
    print(f"filename: {file_name}")

    loader = PDFPlumberLoader(save_file)
    docs = loader.load_and_split()
    print(f"docs len={len(docs)}")

    chunks = text_splitter.split_documents(docs)
    print(f"chunks len={len(chunks)}")

    number_of_documents_deleted = deleteIfFoundByFilename(save_file)
    if number_of_documents_deleted > 0:
        print(f"Deleted existing {save_file}: {number_of_documents_deleted} chunks deleted from vector store")

    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path
    )
    vector_store.persist()

    print(f"Successfully Uploaded {file_name}")
    response = {
        "status": "Successfully Uploaded",
        "filename": file_name,
        "doc_len": len(docs),
        "chunks": len(chunks),
    }
    return response

@app.route("/list", methods=["POST"])
def listPost():
    documents = vector_store.get()
    return {"documents": documents}

def listByFilename(filename):
    documents = vector_store.get(where={"source": filename})
    return documents

def deleteIfFoundByFilename(filename):
    documents = listByFilename(filename)
    if not documents:
        return 0
    document_ids = documents["ids"]
    if not document_ids:
        return 0
    vector_store.delete(document_ids)
    return len(document_ids)

@app.route("/list_by_filename", methods=["POST"])
def list_by_filenamePost():
    json_content = request.json
    filename = json_content.get("filename")
    print(f"filename: {filename}")
    documents = listByFilename(filename)

    return {"documents": documents}

@app.route("/delete", methods=["POST"])
def deletePost():
    json_content = request.json
    filename = json_content.get("filename")
    print(f"filename: {filename}")

    number_of_documents_deleted = deleteIfFoundByFilename(filename)
    
    response = {
        "status": "Successfully Deleted",
        "filename": filename,
        "number_of_documents_deleted": number_of_documents_deleted,
    }
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
