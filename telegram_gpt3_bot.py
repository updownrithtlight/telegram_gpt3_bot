import os
import openai
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Set up your API keys
# Set up your API keys as environment variables
TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# TELEGRAM_API_TOKEN = "6102923737:AAGpHeal1hseouwgl12x_37R6L7ZfxxD68w"
# OPENAI_API_KEY = "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"


openai.api_key = OPENAI_API_KEY

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(fr'Hi {user.mention_markdown_v2()}\! I am a GPT-3 powered chatbot\.')

def gpt3_request(prompt: str) -> str:
    model_engine = "gpt-3.5-turbo"  # You can choose other models like "text-curie-002" or "text-babbage-002"
    messagebody=[
    {"role": "assistant", "content": prompt}
    ]
    completion = openai.ChatCompletion.create(
        model=model_engine,
        messages=messagebody
    )
    logging.info(f"gpt3_request completion received: {completion}")
    message = completion.choices[0].message.content

    return message

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    user_message = update.message.text
    logging.info(f"telegram webhook received: {user_message}")
    prompt = f"{user_message}"
    
    reply = gpt3_request(prompt)
    response = reply.split('\n')
    for res in response:
        update.message.reply_text(res)
    

def main() -> None:
    """Start the bot."""
    updater = Updater(TELEGRAM_API_TOKEN)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM, or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
    logging.info("Starting telegram chatbot server")

