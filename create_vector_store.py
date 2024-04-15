from imports import *
from keys import *
from llm import *

def create_vector_store():
    embed_model = CohereEmbedding(
    cohere_api_key=cohere_api_key,
    model_name="embed-english-v3.0",
    input_type="search_query",
    )
    faiss_index = faiss.IndexFlatL2(d)
    documents = SimpleDirectoryReader("resumes").load_data()
    Settings.embed_model = embed_model
    Settings.chunk_size = 512
    vector_store = FaissVectorStore(faiss_index=faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context,embed_model=embed_model
    )
    index.storage_context.persist()


def query_vector_store(prompt, top_k=2):
    """
    Query the vector store through the query engine to find similar resumes.

    Args:
    - prompt (str): The input prompt to query for similar resumes.
    - top_k (int): The number of similar resumes to retrieve.

    Returns:
    - list[str]: A list of similar resume texts.
    """
    # Use the query engine to query the index with your prompt
    query_engine = index.as_query_engine(similarity_top_k = top_k)
    response = query_engine.query(prompt)

    similar_resumes = []

    # Check if the response includes 'source_nodes', which contain detailed information about similar documents
    if hasattr(response, 'source_nodes'):
        for node_with_score in response.source_nodes:
            # Each node_with_score object should contain a 'node' attribute with the document details
            node = node_with_score.node
            if hasattr(node, 'text'):
                # Append the text of the document to the list of similar resumes
                similar_resumes.append(node.text)

    return similar_resumes