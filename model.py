import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv("api.env")

# Establish database connection
def connect_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            port=int(os.getenv("MYSQL_PORT"))
        )
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Database Connection Failed: {err}")
        return None

# Retrieve response from database
def get_stored_response(question):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "SELECT response FROM conversations WHERE question = %s LIMIT 1"
            cursor.execute(sql, (question,))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"❌ Database Error: {err}")
        finally:
            if cursor:
                cursor.close()
            connection.close()
    return None

# Store only AI-generated responses in the database
def store_conversation(question, response, is_ai_generated=True):
    if not is_ai_generated:
        return  # Only AI responses should be stored
    
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO conversations (question, response) VALUES (%s, %s)"
            cursor.execute(sql, (question, response))
            connection.commit()
            print(f"✅ AI response added to DB: {response}")
        except mysql.connector.Error as err:
            print(f"❌ Database Error: {err}")
        finally:
            if cursor:
                cursor.close()
            connection.close()

# Fetch from DB or generate AI response
def chat_with_bot(question):
    stored_response = get_stored_response(question)
    
    if stored_response:
        return stored_response  
    
    new_response = "I don't know the answer yet, but I'm learning!"
    store_conversation(question, new_response, is_ai_generated=True)
    return new_response

# Test database connection
try:
    connection = connect_db()
    if connection:
        print("✅ Evelyn AI Model Loaded Successfully!")
        connection.close()
except Exception as e:
    print(f"❌ Model Load Failed: {e}")
