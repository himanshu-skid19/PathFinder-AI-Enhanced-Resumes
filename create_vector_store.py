from imports import *
from llm import *
from app import *
from read_data import *



def create_vector_store(directory_path):
    """
    Initialize the vector store and process all PDFs in the directory.
    """
    # Initialize embedding model
    lc_embed_model = HuggingFaceEmbeddings(
       model_name="sentence-transformers/all-mpnet-base-v2"
    )
    embed_model = LangchainEmbedding(lc_embed_model)
    
    # Initialize vector store
    vector_store = FaissVectorStore(faiss.IndexFlatL2(768))  # Example dimension
    
    # Process all PDFs in the directory
    documents = process_directory(directory_path, embed_model, vector_store)
    Settings.embed_model = embed_model
    Settings.chunk_size = 512
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context,embed_model=embed_model
    )
    index.storage_context.persist()
    logging.info("Vector store created and all sections stored.")
    return index
    

def check_vector_store_exists(persist_dir="./storage"):
    """
    Check if the vector store exists in the given directory.
    """
    # This could be more sophisticated depending on how the directory and files are structured
    # Here we simply check if the directory is non-empty
    return os.path.exists(persist_dir) and len(os.listdir(persist_dir)) > 0

def load_vector_store(persist_dir="./storage"):
    """
    Load the existing vector store from the specified persistent directory.

    Args:
        persist_dir (str): The directory where the vector store is persisted.

    Returns:
        index (VectorStoreIndex): The loaded vector store index ready for querying.
    """
    lc_embed_model = HuggingFaceEmbeddings(
       model_name="sentence-transformers/all-mpnet-base-v2"
    )
    embed_model = LangchainEmbedding(lc_embed_model)
    Settings.embed_model = embed_model
    Settings.chunk_size = 512
    # Check if the vector store actually exists in the specified directory
    if not os.path.exists(persist_dir) or not os.listdir(persist_dir):
        raise FileNotFoundError("No vector store found in the specified directory. Please check the path or create a new vector store.")

    # Load the vector store using predefined functions from the llama_index package
    vector_store = FaissVectorStore.from_persist_dir(persist_dir)
    storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=persist_dir)

    # Load the index from the storage context
    index = load_index_from_storage(storage_context=storage_context)

    return index

def query_vector_store(index, top_k=4):
    """
    Query the vector store through the query engine to find similar resumes.

    Args:a
    - prompt (str): The input prompt to query for similar resumes.
    - top_k (int): The number of similar resumes to retrieve.

    Returns:
    - list[str]: A list of similar resume texts.
    """
    # Use the query engine to query the index with your prompt
    # lc_embed_model = HuggingFaceEmbeddings(
    #    model_name="sentence-transformers/all-mpnet-base-v2"
    # )
    # embed_model = LangchainEmbedding(lc_embed_model)
    # Settings.embed_model = embed_model
    # Settings.chunk_size = 512

    

    # query_engine = index.as_query_engine(similarity_top_k = top_k)
    # response = query_engine.query(prompt)
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10,
        )
    


    retrieval_prompt = f"Search for documents which have information relevant to this category and fetch THEM only."
    query_engine = index.as_query_engine(similarity_top_k = 1)
    response = query_engine.query(retrieval_prompt)

    similar_data = []

    # Check if the response includes 'source_nodes', which contain detailed information about similar documents
    if hasattr(response, 'source_nodes'):
        for node_with_score in response.source_nodes:
            # Each node_with_score object should contain a 'node' attribute with the document details
            node = node_with_score.node
            if hasattr(node, 'text'):
                # Append the text of the document to the list of similar resumes
                similar_data.append(node.text)

    return similar_data