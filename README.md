# Voice-RAG-Assistant

A Voice-Enabled Retrieval-Augmented Generation (RAG) Assistant built with Python, Groq, Whisper, and Google Generative AI. This project combines speech recognition, document retrieval, embeddings, large language models, and text-to-speech to create an intelligent voice-based AI assistant capable of answering questions from a custom knowledge base.

## Features

* Voice Input Recording
* Whisper Speech-to-Text (STT)
* Retrieval-Augmented Generation (RAG)
* Document-Based Question Answering
* Embedding-Based Context Retrieval
* Groq LLM Integration
* Google Generative AI Support
* Text-to-Speech (TTS) Responses
* Conversation History Management
* Secure API Key Management with Environment Variables
* Modular and Scalable Architecture

## Architecture

User Voice Input
↓
Whisper Speech-to-Text
↓
Text Embeddings
↓
Document Retrieval
↓
Relevant Context
↓
Groq LLM
↓
Generated Response
↓
Text-to-Speech
↓
Voice Output

## Project Workflow

1. Capture user voice input through the microphone.
2. Convert speech into text using Whisper.
3. Retrieve relevant information from documents using embeddings.
4. Pass retrieved context and user query to the LLM.
5. Generate an accurate response using Groq.
6. Convert the response into speech.
7. Play the generated audio back to the user.

## Technologies Used

* Python
* Groq API
* Whisper
* Google Generative AI
* Text Embeddings
* RAG (Retrieval-Augmented Generation)
* sounddevice
* soundfile
* dotenv

## Installation

Clone the repository:

git clone https://github.com/ujjwal540/Voice-RAG-Assistant.git

Create a virtual environment:

python -m venv .venv

Activate the environment:

Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a .env file:

GROK_API_KEY=your_key_here

GOOGLE_API_KEY=your_key_here

Run the application:

python voice_agent.py

## Example

User Query:

"What is Artificial Intelligence?"

Assistant Response:

"Artificial Intelligence is a branch of computer science focused on creating systems capable of learning, reasoning, and decision-making."

## Future Improvements

* PDF Document Support
* Multiple Document Upload
* FAISS Vector Database Integration
* Streamlit Web Interface
* Real-Time Voice Streaming
* Multi-Language Support
* Source Citations
* Cloud Deployment
* Agentic Workflows
* Web-Based Voice Assistant

## Author

Ujjwal Kumar Karn

AI & Machine Learning Enthusiast | Aspiring AI Engineer
