import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Paths
AUDIO_DIR = "data/audio"
TRANSCRIPT_DIR = "data/transcripts"
CHUNK_DIR = "data/chunks"
DB_DIR = "data/chromadb"

# ChromaDB
CHROMA_COLLECTION_NAME = "video_chunks"

# Model names
WHISPER_MODEL = "base"
OPENAI_MODEL = "gpt-3.5-turbo"

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

openAiClient = OpenAI(api_key=openai_api_key)

import warnings
warnings.filterwarnings("ignore", message="`encoder_attention_mask` is deprecated")
os.environ["TOKENIZERS_PARALLELISM"] = "false"