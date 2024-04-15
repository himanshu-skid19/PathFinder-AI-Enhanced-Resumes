import pdfplumber
import os
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.core import (
    SimpleDirectoryReader,
    load_index_from_storage,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.faiss import FaissVectorStore
from IPython.display import Markdown, display
from llama_index.core import Settings
import faiss
from typing import Any, Sequence
import requests
from llama_index.core.llms import CustomLLM, ChatMessage, ChatResponse, CompletionResponse
from llama_index.core.base.llms.types import CompletionResponseGen, ChatResponseGen
from llama_index.core.llms.callbacks import llm_completion_callback
import streamlit as st
