from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
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
from stqdm import stqdm
import re
from llama_index.llms.anthropic import Anthropic
import logging
from langchain.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.core import Document
import pdfplumber
import csv
from llama_index.core.postprocessor import KeywordNodePostprocessor
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.schema import NodeWithScore
from typing import List, Optional
import anthropic
import json
