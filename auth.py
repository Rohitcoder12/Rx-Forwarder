# auth.py
import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

async def authenticate_user(phone_number, api_id, api_hash):
    client = TelegramClient('session_' + phone_number, api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        try:
            await client.send_code(phone_number)
            code = input('Enter the code: ')
            await client.sign_in(phone_number, code)
        except SessionPasswordNeededError:
            password = input('Enter your password: ')
            await client.sign_in(password=password)
    return client

# Example of sending OTP via Telegram (less reliable)
async def send_otp_telegram(client, phone_number):
    otp = "123456" # Generate a random OTP
    await client.send_message(phone_number, f"Your OTP is: {otp}")
    return otp