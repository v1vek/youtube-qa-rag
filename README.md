# 📺 YouTube Transcription + RAG Question Answering System

This project allows you to ask questions about YouTube videos and get accurate answers by downloading, transcribing, chunking, embedding, and querying the transcript using a Retrieval-Augmented Generation (RAG) pipeline.

## ✨ Features

- Download audio from YouTube videos
- Transcribe speech to text using OpenAI Whisper
- Chunk the transcript into semantic segments
- Embed chunks using `SentenceTransformers`
- Store and retrieve data using `ChromaDB`
- Retrieve top-k relevant chunks for a query
- Generate an answer using OpenAI's GPT model
- Shareable timestamp link to the answer in the video

---

## 🧱 Project Structure

```text
project/
│
├── main.py # Orchestration script
├── ingest/
│ ├── downloader.py # Downloads audio from YouTube
│ ├── transcriber.py # Transcribes audio using Whisper
│ └── chunker.py # Splits transcript into chunks
│
├── vectorstore/
│ ├── embedder.py # Embeds transcript chunks
│ └── db.py # Handles ChromaDB collection
│
├── rag/
│ ├── retriever.py # Retrieves relevant chunks
│ └── answerer.py # Generates answers from chunks
│
├── utils/
│ └── extract_video_id.py # Helper to parse YouTube URL
│
├── config.py # Configuration constants
└── chroma_db/ # Persistent storage for Chroma
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Ensure `ffmpeg` is also installed (for `yt_dlp` to extract audio):

```bash
# On macOS
brew install ffmpeg

# On Ubuntu
sudo apt install ffmpeg
```

## 🛠️ Configuration

Edit config.py to set paths and constants:

```python
# Paths
AUDIO_DIR = "data/audio"
TRANSCRIPT_DIR = "data/transcripts"
CHUNK_DIR = "data/chunks"
DB_DIR = "data/chromadb"

# ChromaDB
CHROMA_COLLECTION_NAME = "youtube_transcripts"

# Model names
WHISPER_MODEL = "base"
OPENAI_MODEL = "gpt-3.5-turbo"
```

### Environment Variables

This project uses an .env file to securely manage sensitive credentials such as your OpenAI API key.

Create a .env file in the root of your project, create a file named .env and add the following line:

```env
OPENAI_API_KEY=your-openai-api-key
```

Replace `your-openai-api-key` with your actual OpenAI key, available at [OpenAI API Keys](https://platform.openai.com/account/api-keys).

## 📦 Usage

Run the main script:

```bash
python main.py \
    --url "<https://www.youtube.com/watch?v=VIDEO_ID>" \
    --query "Whose is director of Maareesan?" \
    --top-k 3
```

Example:

```bash
python main.py \
    --url "<https://www.youtube.com/watch?v=abc123xyz>" \
    --query "What is the example project being shown?" \
    --top-k 3
```

## 📌 How It Works

1. Extract Video ID from the YouTube URL
2. Download Audio using yt_dlp
3. Transcribe Audio using Whisper
4. Chunk Transcript into meaningful segments
5. Embed Chunks using sentence-transformers
6. Store Embeddings in ChromaDB with metadata
7. Query Chunks using semantic search
8. Generate Answer using OpenAI GPT on top-K chunks
9. Print YouTube Timestamp link for the most relevant chunk

## 🧪 Example Output

```yaml
📺 Processing video: SE9jc_haYFo
Downloading audio for video ID: SE9jc_haYFo
Transcribing audio: data/audio/SE9jc_haYFo.mp3
Chunks created and saved to: data/chunks/SE9jc_haYFo.json
Stored 8 chunks in collection 'video_chunks' for video ID: SE9jc_haYFo
Embeddings stored for video ID: SE9jc_haYFo
Retrieved 2 relevant chunks.

💬 Answer:
The director of Maareesan is Sudheesh Shankar. The movie stars popular actors such as Vadivelu and Fahad Fasil. The film is described as having good ideas but struggles with execution, blending elements of a road movie and a social justice thriller. Sudheesh Shankar and the writer, V. Krishnamoorthy, are noted for their ambitious approach to the film.

📚 Sources:
- [0s](https://www.youtube.com/watch?v=SE9jc_haYFo&t=0s): Title sponsor, Grand Royal Toast, powered by the Chinese Six. Hello and welcome to Gallata Plus. In...
- [87s](https://www.youtube.com/watch?v=SE9jc_haYFo&t=87s): that life is made up of memories and there is nothing as terrible as losing a mind slowly. For her t...
```

## ✅ TODO

- [ ] Add caching for transcriptions  
- [ ] Add UI for interactive querying  
- [ ] Add support for multi-video RAG  
- [ ] Add test suite  
