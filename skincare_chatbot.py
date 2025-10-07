import os
import google.generativeai as genai
from dotenv import load_dotenv

# === 1. Load your API key from the .env file ===
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(" No Gemini API key found! Add it to your .env file as GEMINI_API_KEY")

# === 2. Configure Gemini ===
genai.configure(api_key=api_key)

# Use one of your available models (you listed them earlier)
# You can use "models/gemini-2.5-flash" or "models/gemini-2.5-pro"
model = genai.GenerativeModel("models/gemini-2.5-flash")

# === 3. System prompt (this defines your chatbot’s role and boundaries) ===
system_prompt = """
You are SkinCareBot — a friendly AI skincare assistant.
You provide general skincare advice, ingredient information, and daily routine tips.
You are NOT a doctor. Never diagnose or prescribe treatment.
If a user describes a medical condition, tell them to see a dermatologist.
Always keep responses short, clear, safe, and polite.
"""

# === 4. Welcome message ===
print(" Welcome to SkinCareBot! Type 'exit' to quit.\n")

# === 5. Chat loop ===
chat_history = []

while True:
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() in ["exit", "quit"]:
        # print(" Chat history:")
        # for turn in chat_history:
        #     print(f"You: {turn['user']}")
        #     print(f"Skincare Bot: {turn['bot']}\n")

        print(" Goodbye! Take care of your skin.")
        break

    # Build conversation context dynamically
    context = system_prompt + "\n\nConversation so far:\n"
    for turn in chat_history[-5:]:  # remember last 5 turns only
        context += f"User: {turn['user']}\nSkincare Bot: {turn['bot']}\n"
    context += f"User: {user_input}\nSkincare Bot:"

    try:
        # === 6. Generate a response ===
        response = model.generate_content(context)
        bot_reply = response.text.strip()

        # === 7. Display reply ===
        print(f"Skincare Bot: {bot_reply}\n")

        # === 8. Save chat history ===
        chat_history.append({"user": user_input, "bot": bot_reply})

    except Exception as e:
        print(f" Error: {e}\n")
