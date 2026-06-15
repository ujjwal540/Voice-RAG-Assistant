#Document-RAG-Assistant

A Retrieval-Augmented Generation (RAG) chatbot built using Python, Grok API, and Google Generative AI. The chatbot retrieves relevant information from a text document and generates accurate responses based on the document content.

## Features

* Retrieval-Augmented Generation (RAG)
* Question Answering from Documents
* Grok API Integration
* Google Generative AI Integration
* Environment Variable Security
* Simple and Lightweight Implementation
* Easy to Extend for PDFs and Multiple Documents

## Project Workflow

1. Load document data from a text file.
2. Process and store document content.
3. User enters a question.
4. Relevant information is retrieved from the document.
5. Retrieved context is sent to the LLM.
6. The model generates an answer based on the document content.

## Technologies Used

* Python
* Grok API
* Google Generative AI
* dotenv
* RAG Architecture

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/RAG-Powered-Chatbot.git
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate environment:

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a .env file:

```env
GROK_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

Run the project:

```bash
python app.py
```

## Example

Question:

```text
What is Artificial Intelligence?
```

Answer:

```text
Artificial Intelligence is ...
```

## Future Improvements

* Multiple Document Upload
* Streamlit Web Interface
* Vector Database Integration
* Chat History Memory
* Hybrid Search
* Deployment on Cloud

## Author

Ujjwal Kumar Karn

AI & Machine Learning Enthusiast
