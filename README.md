# Evelyn AI Assistant – Conversational Chatbot with Gemini API & LSTM Memory

Evelyn is a minimalist, intelligent AI assistant designed with a unique tone — elegant, mysterious, and emotionally intelligent. She can answer questions, engage in warm conversation, and rephrase responses using the Gemini API to maintain a human-like, poetic style. This project blends deep learning (LSTM), Gemini AI, Flask APIs, MySQL memory, and Wikipedia integration into a beautiful and functional AI chatbot.

## Features

- Natural Language Conversation via Flask API
- LSTM-based Response Model (optional)
- Gemini API Integration for Text Rephrasing
- Wikipedia API Integration for Factual Queries
- MySQL Database for Long-Term Chat Memory
- Environment-safe with `.env` Variables
- Frontend with HTML/CSS for Simple UI

---

## Tech Stack

| Layer       | Tool / Library |
|-------------|----------------|
| Backend     | Python + Flask |
| ML/NLP      | Keras, TensorFlow, LSTM |
| Rephrasing  | Gemini API (Google Generative AI) |
| Database    | MySQL + mysql-connector-python |
| External API| Wikipedia |
| Frontend    | HTML, CSS |
| Deployment  | Localhost / Web Hosting Ready |

---

## Libraries Used

- flask  
- tensorflow  
- keras  
- google-generativeai  
- wikipedia  
- mysql-connector-python  
- python-dotenv  

## **Folder Structure**

Evelyn-AI/

│

├── static/               # CSS/JS files

├── templates/            # HTML frontend

├── .env                  # API keys and DB credentials

├── app.py                # Main Flask App

├── model.py              # LSTM Model (Optional)

├── database.py           # MySQL Interaction Logic

├── gemini_utils.py       # Gemini API Rephrasing Logic

├── wiki.py               # Wikipedia Search

└── README.md             # Project Overview


## **Why This Stack?**

LSTM: Efficient for short conversational memory, and easy to customize.

Gemini API: Adds elegance and human-like touch to replies.

Flask: Lightweight, simple RESTful API framework.

MySQL: Structured memory storage with easy retrieval and scalability.

Wikipedia API: Instant fallback to factual info when needed.


## **Future Plans**

 Add Transformer-based model option

 Deploy on HuggingFace or Vercel

 Enable voice input/output

 Add VR support with 3D Avatar integration

 Train custom tone on Evelyn's unique personality


 ## **Author**

 Abhijith.k
 
 Email: llaiabhijith@gmail.com

 LinkedIn:www.linkedin.com/in/abhijithlin
