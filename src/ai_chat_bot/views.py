import asyncio
import json
import os

import openai
import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from django.shortcuts import render, redirect
from personal_assistant.settings import GTPAPIKEY, TELEGRAM_BOT_TOKEN
from psycopg2 import Error
from aiogram import executor

openai.api_key = GTPAPIKEY
GPT_MODEL = "gpt-3.5-turbo"

if not os.path.exists('ai_chat_bot/users_tg_id.json'):
    with open('ai_chat_bot/users_tg_id.json', 'w') as file:
        json.dump({}, file, indent=4)

TOKEN = TELEGRAM_BOT_TOKEN
bot = Bot(TOKEN, parse_mode="HTML")
dispatcher = Dispatcher(bot)
CURRENT_USER = None


def main(request):
    return render(request=request, template_name='ai_chat_bot/index.html', context={})


@dispatcher.message_handler(commands=["start"])
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    language = message.from_user.locale.language
    print(language)
    hello = 'Hello'
    fullname = message.from_user.full_name
    user_id = message.from_user.id
    info = 'This is massage from your AI Generator.'
    print(user_id)
    print(fullname)
    if os.path.exists('ai_chat_bot/temp_curent_user.txt'):
        with open('ai_chat_bot/temp_curent_user.txt', 'r') as file:
            CURRENT_USER = file.read()

        with open('ai_chat_bot/users_tg_id.json', 'w') as file:
            json.dump({CURRENT_USER: user_id}, file, indent=4)

            os.remove('ai_chat_bot/temp_curent_user.txt')

    await message.answer(f"{hello}, <b>{fullname}!</b>\n"
                         f"{info}")


# @dispatcher.message_handler()
# async def echo_handler(message: types.Message) -> None:
#     """
#     Handler will forward received message back to the sender
#
#     By default, message handler will handle all message types (like text, photo, sticker and etc.)
#     """
#     try:
#         # Send copy of the received message
#         await bot.send_message()
#         await message.send_copy(chat_id=message.from_user.id)
#         await message.answer(text=message.text.upper())
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")


async def on_startup(_):
    print(f'Bot started!')


def run_polling():
    try:
        # logging.basicConfig(level=logging.INFO)
        executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
    except Exception as error:
        print(f'Error name:{error}')


def redirect_check(request, query):
    print(f'{query}')
    global CURRENT_USER
    CURRENT_USER = request.user.id

    with open('ai_chat_bot/users_tg_id.json', 'r') as file:
        telegram_user = json.load(file)
    tg_user_id = telegram_user.get(str(CURRENT_USER))
    if tg_user_id:
        asyncio.run(start_chatting(tg_user_id, CURRENT_USER, contact_id=query))

        return redirect(to="https://t.me/ChefHelperBot")
    with open('ai_chat_bot/temp_curent_user.txt', 'w') as file:
        file.write(str(CURRENT_USER))
    print(f'USER ID FROM REQUEST {CURRENT_USER}')
    return redirect(to="https://t.me/ChefHelperBot")


async def start_chatting(tg_user_id, user_id, contact_id):
    print(f'USER ID:  {user_id}')
    print('START CHATING ' + str(tg_user_id))
    contact = db_connection(user_id, contact_id)
    if contact:

        with open('contact_id.txt', 'w') as file:
            file.write(f'{user_id}:{contact_id}')

        contact_first_name = contact[1]
        contact_last_name = contact[2]
        contact_bday = contact[3]
        # contact_bday = contact[3].strftime("%Y-%m-%d")
        contact_address = contact[6]
        contact_gender = contact[8]
        contact_status = contact[9]
        question = f"Start dialog as your {contact_status} want's to tolk to you?"

        message = generate_ai_message(question, contact_first_name, contact_last_name, contact_bday, contact_address,
                                      contact_gender, contact_status)

        if message:
            await bot.send_message(tg_user_id, message)

        else:
            await bot.send_message(tg_user_id, 'Ups ... haven\'t read prompt well ...')


def generate_ai_message(question, contact_first_name, contact_last_name, contact_bday, contact_address, contact_gender,
                        contact_status):
    promptttt = f"Please answer as a real {contact_status}.Like your first name is {contact_first_name} and last name is {contact_last_name}, currently living in: {contact_address}, with {contact_gender} gender!"

    prompt = f"Answer me as it was written by human with name: {contact_first_name} {contact_last_name}."

    try:
        completion = openai.ChatCompletion.create(

            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.9,
        )
        text = completion.choices[0].message.content
        return text
    except Exception as er:
        print(er)


@dispatcher.message_handler()
async def handle_ai_message(message: types.Message):
    chat_id = message.from_user.id
    print(f'Message from BOT !!!!!!!!!!   {message.text}')
    # history = await bot.forward_message(chat_id, )

    with open('contact_id.txt', 'r') as file:
        user_id, contact_id = file.read().split(':')

        print(f'This is Yur CONTACT ID !!!!!!!!!{user_id}:{contact_id}')

    contact = db_connection(user_id, contact_id)
    if contact:
        contact_first_name = contact[1]
        contact_last_name = contact[2]
        contact_bday = contact[3]
        # contact_bday = contact[3].strftime("%Y-%m-%d")
        contact_address = contact[6]
        contact_gender = contact[8]
        contact_status = contact[9]
        question = message.text

        answer = ''

        for _ in range(3):
            answer = generate_ai_message(question, contact_first_name, contact_last_name, contact_bday, contact_address,
                                         contact_gender, contact_status)
            if answer:
                await bot.send_message(chat_id, answer)
                break


def db_connection(user_id, contact_id):
    connection = None
    cursor = None
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=env('ELEPHANT_DATABASE_USER'),
                                      password=env('ELEPHANT_DATABASE_PASSWORD'),
                                      host=env('ELEPHANT_DATABASE_HOST'),
                                      port=env('ELEPHANT_DATABASE_PORT'),
                                      database=env('ELEPHANT_DATABASE_NAME'))

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute(
            f"SELECT * FROM contactsapp_contact WHERE contactsapp_contact.user_id={user_id} AND contactsapp_contact.id={contact_id}")
        # Fetch result
        record = cursor.fetchone()

        print("You are connected to - ", record, "\n")
        return record
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
