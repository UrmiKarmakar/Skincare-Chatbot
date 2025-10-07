import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# === 1. Load API key ===
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("No Gemini API key found! Add it to your .env file as GEMINI_API_KEY")

genai.configure(api_key=api_key)

# === 2. Model ===
model = genai.GenerativeModel("models/gemini-2.5-flash")

# === 3. System role ===
system_prompt = """
You are SkinCareBot — a friendly AI skincare assistant.
You provide general skincare advice, ingredient information, and daily routine tips.
You are NOT a doctor. Never diagnose or prescribe treatment.
If a user describes a medical condition, tell them to see a dermatologist.
Always keep responses short, clear, safe, and polite.
"""

# === 4. Load previous chat history (persistent memory) ===
def load_history():
    if os.path.exists("chat_history.json"):
        with open("chat_history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open("chat_history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

chat_history = load_history()

print("🧴 Welcome to SkinCareBot! (Now with memory 💾)\nType 'exit' to quit.\n")

# === 5. Chat loop ===
while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        save_history(chat_history)
        print("💾 Chat saved! Goodbye! Take care of your skin 💖")
        break

    # Build context from last few messages
    context = system_prompt + "\n\nConversation so far:\n"
    for turn in chat_history[-5:]:
        context += f"User: {turn['user']}\nSkincare Bot: {turn['bot']}\n"
    context += f"User: {user_input}\nSkincare Bot:"

    try:
        response = model.generate_content(context)
        bot_reply = response.text.strip()
        print(f"Skincare Bot: {bot_reply}\n")

        chat_history.append({"user": user_input, "bot": bot_reply})

    except Exception as e:
        print(f" Error: {e}\n")
