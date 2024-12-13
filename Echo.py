from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai


TOKEN = "7563343667:AAGOC_Ns1hvm-1stodQFwYzp675NdfbbkOk"
API_KEY = "AIzaSyBEoVw4c-mtYwq7WIjcPcYMi3XML9TazzI"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_content(full_prompt: str) -> str:
    try:
        response = model.generate_content(full_prompt)
        return response.text if hasattr(response, 'text') else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"There was an error generating the response: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.first_name
    system_message = f"Hello {user_id}! I am Echo, your friendly chatbot. How can I help you today?"
    await update.message.reply_text(system_message)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()

    
    if "who are you" in user_message or "what are you" in user_message:
        response_text = (
            "I am Echo, a chatbot designed to assist you with your questions and provide interesting conversations! "
            "Feel free to ask me anything."
        )
    else:
        response_text = generate_content(update.message.text)

    await update.message.reply_text(response_text)


app = ApplicationBuilder().token(TOKEN).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))


app.run_polling()
