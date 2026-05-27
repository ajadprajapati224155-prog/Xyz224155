from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
from p_bar import progress_bar
from subprocess import getstatusoutput
from aiohttp import ClientSession
import helper
import time
import asyncio
from pyrogram.types import User, Message
import sys
import re
import os
import master
import random
import datetime
import pytz
import signal
from pyrogram.types import InlineKeyboardButton as key, InlineKeyboardMarkup as m, Message as msg, CallbackQuery
from datetime import datetime
import logging
from aiohttp import ClientSession
from subprocess import getstatusoutput
from typing import Union
import cw, pw
from flask import Flask
from threading import Thread

# ─────────────── FLASK KEEP ALIVE ────────────────────────────────
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

def run():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# ─────────────── LOGGING ─────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

# ─────────────── CONFIG ──────────────────────────────────────────
premium_data = {}
owner_id = int(os.environ.get("OWNER_ID", "6824252172"))

ADMIN_USERNAME   = os.environ.get("ADMIN_USERNAME", "@youradmin")
FORCE_SUB_CHANNEL = os.environ.get("FORCE_SUB_CHANNEL", "your_channel")
SUPPORT_CHANNEL  = os.environ.get("SUPPORT_CHANNEL", "https://t.me/your_support")
ADMIN_LINK       = os.environ.get("ADMIN_LINK", "https://t.me/youradmin")
CHANNEL_ID       = int(os.environ.get("LOG_CHANNEL_ID", "-1002718563674"))

REGION = os.getenv('REGION', 'Asia')

# ─────────────── BOT CLIENT ──────────────────────────────────────
bot = Client(
    "bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH"),
    workers=10
)

# ─────────────── MY PLAN ─────────────────────────────────────────
@bot.on_message(filters.command("myplan"))
async def myplan(client, message: Message):
    user_id = message.from_user.id

    if user_id in premium_data:
        expiry_time = premium_data[user_id]
        expiry_ist = expiry_time.astimezone(pytz.timezone("Asia/Kolkata"))
        expiry_str_in_ist = expiry_ist.strftime("%d-%m-%Y\n⏱️ Expiry time: %I:%M:%S %p")

        current_time = datetime.now(pytz.timezone("Asia/Kolkata"))
        time_left = expiry_ist - current_time

        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_left_str = f"{days} days, {hours} hours, {minutes} minutes"

        await message.reply_text(
            f"Premium user data:\nTime left: {time_left_str}\nExpiry date: {expiry_str_in_ist}"
        )
    else:
        await message.reply_text("You do not have any active premium plan.")


# ─────────────── AUTH / PREMIUM ──────────────────────────────────
def get_seconds(time_str):
    time_parts = time_str.split()
    value = int(time_parts[0])
    unit = time_parts[1].lower()

    if unit.endswith('s'):
        unit = unit[:-1]

    if unit == 'day':
        return value * 86400
    elif unit == 'hour':
        return value * 3600
    elif unit == 'minute' or unit == 'min':
        return value * 60
    elif unit == 'month':
        return value * 2629800
    elif unit == 'year':
        return value * 31557600
    else:
        return 0

@bot.on_message(filters.command("auth"))
async def give_premium_cmd_handler(client, message: Message):
    if message.from_user.id != owner_id:
        await message.reply_text("❌ You are not authorized!")
        return

    if len(message.command) == 4:
        try:
            user_id = int(message.command[1])
            time_val = message.command[2] + " " + message.command[3]
            seconds = get_seconds(time_val)

            if seconds > 0:
                expiry_time = datetime.now() + __import__('datetime').timedelta(seconds=seconds)
                premium_data[user_id] = expiry_time

                expiry_ist = expiry_time.astimezone(pytz.timezone("Asia/Kolkata"))
                expiry_str_in_ist = expiry_ist.strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")
                current_time = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : %I:%M:%S %p")

                user = await client.get_users(user_id)
                await message.reply_text(
                    f"ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅\n\n👤 ᴜꜱᴇʀ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time_val}</code>\n\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}",
                    disable_web_page_preview=True
                )
                await client.send_message(
                    chat_id=user_id,
                    text=f"👋 ʜᴇʏ {user.mention},\nᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴘᴜʀᴄʜᴀꜱɪɴɢ ᴘʀᴇᴍɪᴜᴍ.\nᴇɴᴊᴏʏ !! ✨🎉\n\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time_val}</code>\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}",
                    disable_web_page_preview=True
                )
                try:
                    await client.send_message(
                        chat_id=CHANNEL_ID,
                        text=f"#Added_Premium\n\n👤 ᴜꜱᴇʀ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time_val}</code>\n\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}",
                        disable_web_page_preview=True
                    )
                except Exception:
                    pass
            else:
                await message.reply_text("Invalid time format. Use: /auth user_id 1 day")
        except ValueError:
            await message.reply_text("Invalid user ID or time format!")
    else:
        await message.reply_text("Usage: /auth user_id time\nExample: /auth 123456 1 day")


# ─────────────── CHECK PREMIUM ───────────────────────────────────
@bot.on_message(filters.command("cheak"))
async def chk_premium(client: Client, message: Message):
    if message.from_user.id != owner_id:
        await message.reply_text("❌ Not authorized!")
        return

    if len(message.text.split()) == 1:
        response_text = "Premium Users:\n"
        for uid, expiry_time in premium_data.items():
            try:
                user = await client.get_users(uid)
                expiry_ist = expiry_time.astimezone(pytz.timezone("Asia/Kolkata"))
                expiry_str = expiry_ist.strftime("%d-%m-%Y %I:%M:%S %p")
                current_time = datetime.now(pytz.timezone("Asia/Kolkata"))
                time_left = expiry_ist - current_time
                days = time_left.days
                hours, rem = divmod(time_left.seconds, 3600)
                minutes, _ = divmod(rem, 60)
                response_text += (
                    f"User: {user.username or 'N/A'} | ID: {uid}\n"
                    f"Time left: {days}d {hours}h {minutes}m\n"
                    f"Expiry: {expiry_str}\n\n"
                )
            except Exception:
                response_text += f"User ID: {uid} (error fetching)\n\n"

        await message.reply_text(response_text if response_text != "Premium Users:\n" else "No premium users found!")

    elif len(message.text.split()) == 2:
        try:
            uid = int(message.text.split()[1])
            if uid in premium_data:
                expiry_time = premium_data[uid]
                expiry_ist = expiry_time.astimezone(pytz.timezone("Asia/Kolkata"))
                expiry_str = expiry_ist.strftime("%d-%m-%Y %I:%M:%S %p")
                current_time = datetime.now(pytz.timezone("Asia/Kolkata"))
                time_left = expiry_ist - current_time
                days = time_left.days
                hours, rem = divmod(time_left.seconds, 3600)
                minutes, _ = divmod(rem, 60)
                await message.reply_text(
                    f"User ID: {uid}\nTime left: {days}d {hours}h {minutes}m\nExpiry: {expiry_str}"
                )
            else:
                await message.reply_text("No premium data found for this user!")
        except ValueError:
            await message.reply_text("Invalid user ID!")
    else:
        await message.reply_text("Usage:\n/cheak — List all\n/cheak user_id — Check one")


# ─────────────── EXPIRY CHECKER ──────────────────────────────────
async def check_expiry():
    while True:
        await asyncio.sleep(60)
        current_time = datetime.now(pytz.timezone("Asia/Kolkata"))
        expired_users = [
            (uid, exp) for uid, exp in premium_data.items()
            if exp.astimezone(pytz.timezone("Asia/Kolkata")) <= current_time
        ]
        for uid, expiry_time in expired_users:
            try:
                expiry_str = expiry_time.strftime("%d-%m-%Y %I:%M:%S %p")
                try:
                    await bot.send_message(
                        chat_id=CHANNEL_ID,
                        text=f"Premium expired for User ID: {uid}\nExpiry: {expiry_str}"
                    )
                except Exception:
                    pass
                try:
                    await bot.send_message(
                        chat_id=owner_id,
                        text=f"Premium expired for User ID: {uid}\nExpiry: {expiry_str}"
                    )
                except Exception:
                    pass
                del premium_data[uid]
                LOG.info(f"Removed expired premium user: {uid}")
            except Exception as e:
                LOG.error(f"Error in expiry check: {e}")


# ─────────────── LOGS ────────────────────────────────────────────
@bot.on_message(filters.command("logs"))
async def send_logs(client: Client, m: Message):
    if m.from_user.id != owner_id:
        await m.reply_text("❌ Not authorized!")
        return
    try:
        with open("Assist.txt", "rb") as file:
            sent = await m.reply_text("**📤 Sending logs...**")
            await m.reply_document(document=file)
            await sent.delete(True)
    except FileNotFoundError:
        await m.reply_text("No log file found.")
    except Exception as e:
        await m.reply_text(f"Error: {e}")


# ─────────────── FORCE JOIN ──────────────────────────────────────
async def check_force_join(client, user_id):
    try:
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        if member.status in ["kicked", "left"]:
            return False
        return True
    except Exception:
        return False

async def send_force_join_msg(message):
    await message.reply_photo(
        photo="https://te.legra.ph/file/666b524fee02e1accd2fe.png",
        caption=(
            "🚀 **Bot Use Karne Ke Liye Pehle Join Karo!**\n\n"
            "👇 Niche Button Pe Click Karke Channel Join Karo\n"
            "Phir Dobara /start Bhejo ✅"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL}")],
            [InlineKeyboardButton("🔄 Joined? Click Here", callback_data="check_join")]
        ])
    )


# ─────────────── START ───────────────────────────────────────────
@bot.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user_id = message.from_user.id
    is_joined = await check_force_join(client, user_id)
    if not is_joined:
        await send_force_join_msg(message)
        return

    chat_id = message.chat.id
    first_name = message.from_user.first_name or "Dear"
    tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(tz).strftime("%Y-%m-%d %I:%M:%S %p")

    await client.send_photo(
        chat_id=chat_id,
        photo="https://te.legra.ph/file/666b524fee02e1accd2fe.png",
        caption=(
            f"**Hello {first_name} 👋!**\n\n"
            "⚡ **Shiv Extract Bot** — Super Fast TXT Uploader\n\n"
            "📋 **Available Commands:**\n"
            "╔══════════════════╗\n"
            "║ /drm  — DRM Video Downloader\n"
            "║ /txt  — Message to TXT File\n"
            "║ /vpdf — Video to PDF\n"
            "║ /convert — File Convert\n"
            "║ /h2t  — HTML to TXT\n"
            "║ /myplan — My Premium Plan\n"
            "╚══════════════════╝\n\n"
            "💎 **Admin Commands:**\n"
            "╔══════════════════╗\n"
            "║ /auth  — Premium Do\n"
            "║ /cheak — Premium Check\n"
            "║ /logs  — Bot Logs\n"
            "║ /restart — Bot Restart\n"
            "╚══════════════════╝"
        ),
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📢 Support Channel", url=SUPPORT_CHANNEL),
                InlineKeyboardButton("👑 Admin", url=ADMIN_LINK)
            ],
            [
                InlineKeyboardButton("⚔️ /drm — Start Download", callback_data="start_drm")
            ]
        ])
    )


# ─────────────── JOIN CHECK CALLBACK ─────────────────────────────
@bot.on_callback_query(filters.regex("^check_join$"))
async def check_join_callback(client, callback_query):
    user_id = callback_query.from_user.id
    is_joined = await check_force_join(client, user_id)
    if is_joined:
        await callback_query.message.delete()
        await callback_query.answer("✅ Joined! Welcome!", show_alert=True)
        await start_command(client, callback_query.message)
    else:
        await callback_query.answer("❌ Abhi Join Nahi Kiya! Pehle Join Karo.", show_alert=True)


# ─────────────── DRM ─────────────────────────────────────────────
@bot.on_callback_query(filters.regex("^start_drm$"))
async def start_drm_callback(client, callback_query):
    await callback_query.message.delete()
    await drm_app(client, callback_query.message)

@bot.on_message(filters.command("drm"))
async def drm_app(client, message: Message):
    chat_id = message.chat.id
    imoji = await client.send_message(chat_id=chat_id, text="⚔️" * 50)
    await asyncio.sleep(1)
    await client.delete_messages(chat_id=chat_id, message_ids=[imoji.id])
    await send_random_photo(client, chat_id)

async def send_random_photo(client, chat_id):
    width = random.randint(1100, 1250)
    height = random.randint(600, 800)
    reply_markup = gen_drm_kb()
    tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(tz).strftime("%Y-%m-%d %I:%M:%S %p")

    await client.send_photo(
        chat_id=chat_id,
        photo=f"https://picsum.photos/{width}/{height}.jpg",
        caption=(
            f"**Hi👋, DEAR USER 👨‍💻**\n"
            f"**📅 DATE AND TIME: `{current_time}`**\n\n"
            "**⚡ I AM SUPER FAST ⚔️ TXT UPLOADER**\n\n"
            "**➠ 𝐌𝐚𝐝𝐞 𝐁𝐲: ⚔️ Shiv Extract Bot**"
        ),
        reply_markup=reply_markup
    )

def gen_drm_kb():
    keyboard = [
        [key("【 AppX 】", callback_data="appx"), key("【 Pw / Vission 】", callback_data="pw")],
        [key("【 Classplus 】", callback_data="classplus"), key("【 Cp Token 】", callback_data="cp")],
        [key("【 khan 】", callback_data="khan"), key("【 ADDA / IFAS 】", callback_data="adda")],
        [key("【 CW 】", callback_data="cw"), key("【 Uthkarsh 】", callback_data="utk")],
        [key("【 All NON DRM 】", callback_data="non_drm"), key("【 CPVOD DRM 】", callback_data="cpvod")]
    ]
    return m(keyboard)


# ─────────────── CALLBACKS ───────────────────────────────────────
@bot.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    if data in ["check_join", "start_drm"]:
        return  # handled by specific handlers above

    await callback_query.message.delete()

    if data == "appx":
        await callback_query.answer("You chose AppX")
        await handle_appx_logic(client, callback_query.message)
    elif data == "cw":
        await callback_query.answer("You chose Career Will")
        await cw.handle_cw_logic(client, callback_query.message)
    elif data == "pw":
        await callback_query.answer("Physics Wallah / VISION IAS")
        await pw.handle_pw_logic(client, callback_query.message)
    elif data == "classplus":
        await callback_query.answer("You chose ClassPlus")
        await handle_classplus_logic(client, callback_query.message)
    elif data == "khan":
        await callback_query.answer("You chose KHAN GLOBAL STUDIES")
        await handle_khan_logic(client, callback_query.message)
    elif data == "adda":
        await callback_query.answer("You chose Adda247")
        await handle_adda_logic(client, callback_query.message)
    elif data == "utk":
        await callback_query.answer("You chose UTHKARSH CLASSES")
        await handle_utk_logic(client, callback_query.message)


# ─────────────── CONVERT ─────────────────────────────────────────
@bot.on_message(filters.command("convert") & filters.private)
async def handle_convert(client: Client, message: Message):
    await convert_command(client, message)


# ─────────────── H2T ─────────────────────────────────────────────
@bot.on_message(filters.command('h2t'))
async def run_bot(client: Client, m: Message):
    from bs4 import BeautifulSoup
    editable = await m.reply_text("Send Your HTML file\n")
    input_msg: Message = await client.listen(editable.chat.id)
    html_file = await input_msg.download()
    await input_msg.delete(True)
    await editable.delete()
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
        tables = soup.find_all('table')
        videos = []
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    name = cols[0].get_text().strip()
                    link_tag = cols[1].find('a')
                    if link_tag:
                        link = link_tag.get('href', '')
                        videos.append(f'{name}:{link}')
    txt_file = os.path.splitext(html_file)[0] + '.txt'
    with open(txt_file, 'w') as f:
        f.write('\n'.join(videos))
    await m.reply_document(document=txt_file, caption="Here is your txt file.")
    os.remove(txt_file)


# ─────────────── RESTART / STOP ──────────────────────────────────
@bot.on_message(filters.command("stop"))
async def stop_handler(_, m: Message):
    if m.from_user.id != owner_id:
        await m.reply_text("❌ Not authorized!")
        return
    await m.reply_text("⚔️ **STOPPED** ⚔️", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("restart"))
async def restart_handler(_, m: Message):
    if m.from_user.id != owner_id:
        await m.reply_text("❌ Not authorized!")
        return
    await m.reply_text("**⚔️ RESTARTED ⚔️**", True)
    os.execv(sys.executable, ['python'] + sys.argv)


# ─────────────── TXT ─────────────────────────────────────────────
@bot.on_message(filters.command("txt"))
async def account_login(client: Client, m: Message):
    try:
        editable = await m.reply_text('**SEND ME MESSAGE TO CONVERT INTO TXT FILE 🗃️**')
        input_msg: Message = await client.listen(editable.chat.id)
        raw_text = input_msg.text
        await input_msg.delete(True)

        await editable.edit("SEND ME NAME OF TXT FILE ⚡")
        input_msg2: Message = await client.listen(editable.chat.id)
        raw_text0 = input_msg2.text
        await input_msg2.delete(True)
        await editable.delete()

        file_name = f"{raw_text0}.txt"
        with open(file_name, "w") as file:
            file.write(raw_text)

        await client.send_document(chat_id=m.chat.id, document=open(file_name, "rb"), caption="⚔️ Shiv Extract Bot")
        os.remove(file_name)
    except Exception as e:
        await m.reply_text('Failed: ' + str(e))


# ─────────────── APPX LOGIC ──────────────────────────────────────
async def handle_appx_logic(client: Client, m: Message):
    editable = await m.reply_text('**𝗦𝗘𝗡𝗗 𝗧𝗫𝗧 𝗙𝗜𝗟𝗘 🗂**')
    input_msg: Message = await client.listen(editable.chat.id)
    x = await input_msg.download()
    await input_msg.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    path = f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = [i.split("://", 1) for i in content if i.strip()]
        os.remove(x)
    except Exception:
        await m.reply_text("Invalid file input.")
        try:
            os.remove(x)
        except Exception:
            pass
        return

    await editable.edit(
        f"𝗧𝗢𝗧𝗔𝗟 𝗟𝗜𝗡𝗞𝗦: **{len(links)}**\n\n✍️ 𝗡𝗢𝗪 𝗦𝗘𝗡𝗗 𝗦𝗧𝗔𝗥𝗧 𝗡𝗨𝗠𝗕𝗘𝗥 (initial is 1)"
    )
    input0: Message = await client.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**📲 ENTER APP NAME ⚔️**\n**OR SEND `r` for default**")
    input9: Message = await client.listen(editable.chat.id)
    raw_text9 = input9.text
    await input9.delete(True)
    app_name = "⚔️ APPX" if raw_text9.strip() == "r" else (raw_text9.strip() or "⚔️ APPX")

    await editable.edit("**𝗘𝗡𝗧𝗘𝗥 𝗖𝗢𝗨𝗥𝗦𝗘 𝗡𝗔𝗠𝗘 📝 𝗢𝗥 𝗦𝗘𝗡𝗗 `d` 𝗧𝗢 𝗚𝗥𝗔𝗕 𝗙𝗥𝗢𝗠 𝗙𝗜𝗟𝗘**")
    input1: Message = await client.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    b_name = file_name if raw_text0 == 'd' else raw_text0

    await editable.edit("**𝗘𝗡𝗧𝗘𝗥 𝗬𝗢𝗨𝗥 𝗡𝗔𝗠𝗘 ✍️**")
    input3: Message = await client.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    MR = raw_text3.strip() or "⚔️ Bot"

    await editable.edit(
        "𝗡𝗢𝗪 𝗦𝗘𝗡𝗗 🖼️ **𝗧𝗛𝗨𝗠𝗕𝗡𝗔𝗜𝗟 𝗨𝗥𝗟**\n\nEx: `https://graph.org/file/xyz.jpg`\n\n𝗢𝗥 𝗦𝗘𝗡𝗗 `no`"
    )
    input6: Message = await client.listen(editable.chat.id)
    thumb_url = input6.text
    await input6.delete(True)
    await editable.delete()

    if thumb_url.startswith("http://") or thumb_url.startswith("https://"):
        getstatusoutput(f"wget '{thumb_url}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = None

    count = 1 if len(links) == 1 else int(raw_text)

    try:
        for i in range(count - 1, len(links)):
            if len(links[i]) < 2:
                count += 1
                continue

            V = links[i][1].replace("file/d/", "uc?export=download&id=").replace(
                "www.youtube-nocookie.com/embed", "youtu.be"
            ).replace("?modestbranding=1", "").replace("/view?usp=sharing", "")
            url = "https://" + V

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace(
                "#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace(
                "https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {MR} {name1[:60]}'

            if "youtu" in url:
                ytf = "b[height<=480][ext=mp4]/bv[height<=480][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = "b[height<=480]/bv[height<=]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp "{url}" -o "{name}.mp4" --cookies cookies.txt'

            cc = (
                f'**[ 🎥 ] Lᴇᴄ ɪᴅ. »** {str(count).zfill(3)}\n'
                f'**📲 APP NAME - {app_name}**\n\n'
                f'**Title » {name1}**\n\n'
                f'**```BATCH: {b_name}```**\n'
                f'**💎 Downloaded By » {MR}**\n\n'
            )
            cc1 = (
                f'**[ 📁 ] Pᴅғ ɪᴅ. »** {str(count).zfill(3)}\n'
                f'**📲 APP NAME - {app_name}**\n\n'
                f'**Title » {name1}**\n\n'
                f'**```BATCH: {b_name}```**\n'
                f'**💎 Downloaded By » {MR}**\n\n'
            )

            try:
                if "drive" in url:
                    ka = await helper.download(url, name)
                    await client.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                    count += 1
                    os.remove(ka)
                    time.sleep(1)
                elif ".mp3" in url:
                    cmd_mp3 = f'yt-dlp -x --audio-format mp3 -o "{name}.mp3" "{url}" -R 25 --fragment-retries 25'
                    os.system(cmd_mp3)
                    await client.send_document(chat_id=m.chat.id, document=f'{name}.mp3', caption=cc)
                    count += 1
                    os.remove(f'{name}.mp3')
                elif ".pdf" in url:
                    cmd_pdf = f'yt-dlp -o "{name}.pdf" "{url}" -R 25 --fragment-retries 25'
                    os.system(cmd_pdf)
                    await client.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                    count += 1
                    os.remove(f'{name}.pdf')
                else:
                    remaining = len(links) - (i + 1)
                    show_msg = (
                        f"**Downloading ⚔️ ⏬**\n\n"
                        f"**🚀 Link No:** {str(count).zfill(3)}\n"
                        f"**Title:** {name}\n\n"
                        f"**🍁 Total:** {len(links)} | **🌡️ Remaining:** {remaining}\n"
                    )
                    res_file = await helper.download_video(url, cmd, name)
                    prog = await m.reply_text(show_msg)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(client, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)
            except FloodWait as e:
                await m.reply_text(str(e))
                time.sleep(e.value)
                continue
            except Exception as e:
                await m.reply_text(
                    f"**⚠️ Failed**\n\n{str(e)}\n\n**Lec:** {name}\n**Link:** `{url}`"
                )
                continue
    except Exception as e:
        await m.reply_text(str(e))

    await m.reply_text("**⚔️ Successfully Downloaded All Lectures! ⚔️**")


# ─────────────── VPDF ────────────────────────────────────────────
@bot.on_message(filters.command("vpdf"))
async def vision_pdf(client: Client, m: Message):
    editable = await m.reply_text(
        f"☞ I'm **Vision Pdf** Downloader Bot.\n\nSend your TXT file 📄"
    )
    input_msg: Message = await client.listen(editable.chat.id)
    x = await input_msg.download()
    await input_msg.delete(True)

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = [i.split(":", 1) for i in content if i.strip()]
        os.remove(x)
    except Exception:
        await m.reply_text("Invalid file input.")
        try:
            os.remove(x)
        except Exception:
            pass
        return

    await editable.edit(f"Total links: {len(links)}\n\nSend start number (initial is 1)")
    input1: Message = await client.listen(editable.chat.id)
    count = int(input1.text)

    await m.reply_text("**Enter Your Batch Name**")
    inputy: Message = await client.listen(editable.chat.id)
    raw_texty = inputy.text

    await m.reply_text("**Enter Cookie (PHPSESSID)**")
    input2: Message = await client.listen(editable.chat.id)
    cookie = input2.text
    cookies = {'PHPSESSID': f'{cookie}'}

    try:
        for i in range(count, len(links)):
            if len(links[i]) < 2:
                count += 1
                continue
            url = links[i][1]
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace(
                "+", "").replace("#", "").replace("|", "").replace("@", "").replace(
                "*", "").replace(".", "").strip()[:57]
            name = f'{str(count).zfill(3)}) {name1}'
            cc = f'{str(count).zfill(3)}. {name1}.pdf\n\n**Batch:** {raw_texty}\n\n**Extracted By ➤** Shiv Extract Bot'
            ka = await helper.vision(url, name, cookies)
            await m.reply_document(ka, caption=cc)
            count += 1
            os.remove(ka)
    except Exception as e:
        await m.reply_text(str(e))

    await m.reply_text("⚔️ Successfully Downloaded All! ⚔️")


# ─────────────── STUB HANDLERS (placeholders) ────────────────────
async def handle_classplus_logic(client, m):
    await m.reply_text("ClassPlus handler - implement in helper.py")

async def handle_khan_logic(client, m):
    await m.reply_text("Khan handler - implement in helper.py")

async def handle_adda_logic(client, m):
    await m.reply_text("Adda247 handler - implement in helper.py")

async def handle_utk_logic(client, m):
    await m.reply_text("Uthkarsh handler - implement in helper.py")

async def convert_command(client, message):
    await message.reply_text("Convert handler - implement as needed")


# ─────────────── MAIN ────────────────────────────────────────────
async def main():
    keep_alive()
    asyncio.get_event_loop().create_task(check_expiry())
    await bot.start()
    LOG.info("Bot started!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    bot.run()
