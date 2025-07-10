# bot.py
import asyncio
import telebot
from telethon import TelegramClient
from auth import authenticate_user
from database import create_table, add_user, get_user
from config import api_id, api_hash, bot_token

# Initialize Telethon client and Telebot
bot = telebot.TeleBot(bot_token)
clients = {}  # Store Telethon clients for each user

create_table()

@bot.message_handler(commands=['start'])
def start(message):
    phone_number = message.from_user.phone_number
    if not phone_number:
        bot.reply_to(message, "Please set your phone number in Telegram settings.")
        return

    user_data = get_user(phone_number)
    if user_data:
        session_id = user_data[0]
        bot.reply_to(message, f"You are already logged in. Session ID: {session_id}")
    else:
        bot.reply_to(message, "Please log in using /login.")

@bot.message_handler(commands=['login'])
def login(message):
    phone_number = message.from_user.phone_number
    if not phone_number:
        bot.reply_to(message, "Please set your phone number in Telegram settings.")
        return

    if phone_number in clients:
        bot.reply_to(message, "You are already logged in.")
        return

    async def login_user():
        client = await authenticate_user(phone_number, api_id, api_hash)
        clients[phone_number] = client
        add_user(phone_number, client.session.save(), "{}") # Store session
        bot.reply_to(message, "Login successful!")

    asyncio.create_task(login_user())

@bot.message_handler(commands=['setforward'])
def set_forward(message):
    phone_number = message.from_user.phone_number
    if not phone_number or phone_number not in clients:
        bot.reply_to(message, "Please log in first using /login.")
        return

    # Parse the forward rule from the message (e.g., /setforward source_channel_username destination_channel_username)
    try:
        parts = message.text.split()
        source_channel = parts[1]
        destination_channel = parts[2]
        forward_rules = f'{{"{source_channel}": "{destination_channel}"}}'
        add_user(phone_number, clients[phone_number].session.save(), forward_rules)
        bot.reply_to(message, f"Forward rule set: {source_channel} -> {destination_channel}")
    except IndexError:
        bot.reply_to(message, "Invalid format. Use /setforward source_channel destination_channel")

# Add a function to handle the actual forwarding logic
# This will need to run in a loop, checking for new messages in the source channels
# and forwarding them to the destination channels.

# Start the bot
bot.infinity_polling()