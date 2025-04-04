import os
import json
import numpy as np
import tensorflow as tf
import wikipediaapi
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from dotenv import load_dotenv
from model import chat_with_bot, store_conversation
from evelyn_rephrase import rephrase_as_evelyn

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ Missing Gemini API Key. Check your .env file.")

genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)

# Load AI Model
try:
    model = tf.keras.models.load_model("evelyn_lstm.keras")
    print("✅ AI Model Loaded Successfully!")
except Exception as e:
    print(f"❌ Error Loading AI Model: {e}")
    exit()

# Load Tokenizer
try:
    with open("tokenizer.json", "r") as f:
        tokenizer = tokenizer_from_json(f.read())
    print("✅ Tokenizer Loaded Successfully!")
except Exception as e:
    print(f"❌ Error Loading Tokenizer: {e}")
    exit()

max_len = model.input_shape[1]
reverse_word_index = {v: k for k, v in tokenizer.word_index.items()}

# Wikipedia Setup
wiki = wikipediaapi.Wikipedia(language='en', user_agent="EvelynBot/1.0")

# User-defined memory (Stores facts like "Mubashir is my friend")
user_memory = {}

# Define basic responses
basic_responses = {
    "hi": "Greetings, traveler. What do you seek?",
    "hello": "Ah, a familiar presence. What wisdom do you seek?",
    "hey": "Hey yourself. What’s on your mind?",
}

def search_wikipedia(query):
    """Fetch a Wikipedia summary but DO NOT store it."""
    if query.lower() in basic_responses:
        return None  # Skip Wikipedia for common greetings

    page = wiki.page(query)
    if page.exists():
        summary = page.summary.split(". ")[:2]  # Limit to 2 sentences
        print(f"✅ Wikipedia result found for: {query}")
        return ". ".join(summary) + "."
    return None

def store_fact(user_input):
    """Extract and store user-defined facts (e.g., 'Mubashir is my friend')."""
    words = user_input.split()
    
    # Add basic memory: Store general facts like "Alice is my sister"
    if " is my " in user_input:
        parts = user_input.split(" is my ")
        if len(parts) == 2:
            name = parts[0].strip().title()
            relation = parts[1].strip().rstrip(".!")
            user_memory[name.lower()] = f"{name} is your {relation}."
            return f"Noted. {name} is your {relation}."


def retrieve_fact(user_input):
    """Check if the user is asking about a stored entity."""
    words = user_input.lower().split()
    
    for word in words:
        if word in user_memory:
            return user_memory[word]  # Return stored fact

    return None  # No stored fact found

def generate_response(user_input):
    """Smart response system: DB → Fact Memory → Wikipedia → AI Model, with Evelyn-style rephrasing only for AI-generated content."""
    user_input = user_input.strip().lower()

    # 1️⃣ Store new facts (if detected)
    stored_fact = store_fact(user_input)
    if stored_fact:
        return stored_fact  # Acknowledges the stored fact

    # 2️⃣ Retrieve a stored fact if asked
    retrieved_fact = retrieve_fact(user_input)
    if retrieved_fact:
        return retrieved_fact  

    # 3️⃣ Basic Responses
    if user_input in basic_responses:
        return basic_responses[user_input]

    # 4️⃣ Database Check
    stored_response = chat_with_bot(user_input)
    if stored_response and stored_response != "I don't know the answer yet, but I'm learning!":
        return stored_response  

    # 5️⃣ Wikipedia Search
    wiki_response = search_wikipedia(user_input.title())
    if wiki_response:
        return rephrase_as_evelyn(wiki_response)  # ✅ Fixed

    # 6️⃣ Gemini AI Fallback (Handles Copyright Issues)
    try:
        genai_model = genai.GenerativeModel("gemini-1.5-pro")
        response_obj = genai_model.generate_content(user_input)

        if not response_obj.candidates or response_obj.candidates[0].finish_reason == 4:
            print(f"❌ Gemini API blocked response due to copyright. Query: {user_input}")
            raise ValueError("Gemini refused response due to copyright.")

        response = response_obj.text.strip()
        store_conversation(user_input, response)  
        return rephrase_as_evelyn(response)  # ✅ Fixed

    except Exception as e:
            print(f"❌ Gemini API Error: {e}")
            return "Something interrupted my thoughts... try again?"

    # 7️⃣ LSTM AI Model Fallback
    seq = tokenizer.texts_to_sequences([user_input])
    seq = pad_sequences(seq, maxlen=max_len, padding='post')
    prediction = model.predict(seq)

    predicted_indices = np.argmax(prediction, axis=-1)[0]
    response_words = [reverse_word_index.get(idx, "") for idx in predicted_indices if idx]

    if "<end>" in response_words:
        response_words = response_words[:response_words.index("<end>")]

    response = " ".join(response_words).strip()
    if not response or len(response.split()) < 4:
        response = "I'm still learning, but I'll improve over time!"

    return response  

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    response = generate_response(user_message)
    return jsonify({"response": response})

# Startup Test
if __name__ == "__main__":
    print("🔍 Testing Wikipedia Integration...")
    test_query = "Alan Turing"
    print(search_wikipedia(test_query) or "Wikipedia did not return results.")
    app.run(debug=True, use_reloader=False)
