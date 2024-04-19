from imports import *
from app import *

logging.basicConfig(level=logging.INFO)
os.environ["ANTHROPIC_API_KEY"] = "INSERT KEY HERE"
tokenizer = Anthropic().tokenizer
Settings.tokenizer = tokenizer

anthropic_llm = Anthropic(model="claude-3-sonnet-20240229")

Settings.llm = anthropic_llm
