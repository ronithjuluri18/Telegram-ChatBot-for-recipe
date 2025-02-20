import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Set your Telegram bot token and Edamam API key as environment variables
TELEGRAM_TOKEN = '6681185942:AAHH9UihThOrxpkoo2FKn2I1zV1eJ2YKcN0'
EDAMAM_API_KEY = '7150343663c53664878b90561e56556c'

# Define the command handlers
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hi! I'm your recipe bot. Type /recipe <dish_name> to get a recipe.")

def recipe(update: Update, context: CallbackContext) -> None:
    dish_name = " ".join(context.args)
    if not dish_name:
        update.message.reply_text("Please provide a dish name. Example: /recipe spaghetti")
        return

    # Fetch recipe from Edamam API
    endpoint = "https://api.edamam.com/search"
    params = {
        "q": dish_name,
        "app_id": "7b59ad5f",
        "app_key": EDAMAM_API_KEY,
        "from": 0,
        "to": 1,
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if "hits" in data and data["hits"]:
        recipe_title = data["hits"][0]["recipe"]["label"]
        recipe_url = data["hits"][0]["recipe"]["url"]
        update.message.reply_text(f"Here's a recipe for {dish_name}: {recipe_title}\n{recipe_url}")
    else:
        update.message.reply_text(f"Sorry, I couldn't find a recipe for {dish_name}.")

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("recipe", recipe))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
