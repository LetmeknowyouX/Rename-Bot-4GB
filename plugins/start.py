from datetime import date as date_
import datetime
import os
import asyncio
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from helper.database import find_one, insert, used_limit, total_user, daily
from helper.date import check_expi
from config import BOT_USERNAME, FORCE_SUBS, LOG_CHANNEL, BOT_PIC, BOT_TOKEN

bot_username = BOT_USERNAME
log_channel = LOG_CHANNEL
token = BOT_TOKEN
botid = token.split(':')[0]

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user_id = message.chat.id
    insert(int(user_id))
    
    try:
        id = message.text.split(' ')[1]
    except IndexError:
        id = None

    loading_sticker_message = await message.reply_sticker("CAACAgIAAxkBAALmzGXSSt3ppnOsSl_spnAP8wHC26jpAAJEGQACCOHZSVKp6_XqghKoHgQ")
    await asyncio.sleep(2)
    await loading_sticker_message.delete()
    txt = f"""Hello {message.from_user.mention} \n\n➻ This Is An Advanced And Yet Powerful Rename Bot.\n\n➻ Using This Bot You Can Rename And Change Thumbnail Of Your Files.\n\n➻ You Can Also Convert Video To File Aɴᴅ File To Video.\n\n➻ This Bot Also Supports Custom Thumbnail And Custom Caption.\n\n<b>Bot Is Made By @Madflix_Bots</b>"""
    await message.reply_photo(photo=BOT_PIC,
                                caption=txt,
                                reply_markup=InlineKeyboardMarkup(
                                        [[InlineKeyboardButton("📢 Updates", url="https://t.me/Madflix_Bots"),
                                        InlineKeyboardButton("💬 Support", url="https://t.me/MadflixBots_Support")],
                                        [InlineKeyboardButton("🛠️ Help", callback_data='help'),
				                        InlineKeyboardButton("❤️‍🩹 About", callback_data='about')],
                                        [InlineKeyboardButton("🧑‍💻 Developer 🧑‍💻", url="https://t.me/CallAdminRobot")]
                                        ]))
    return

@Client.on_message((filters.private & (filters.document | filters.audio | filters.video)) | filters.channel & (filters.document | filters.audio | filters.video))
async def send_doc(client, message):
    update_channel = FORCE_SUBS
    user_id = message.from_user.id
    if update_channel:
        try:
            await client.get_chat_member(update_channel, user_id)
        except UserNotParticipant:
            _newus = find_one(message.from_user.id)
            user = _newus["usertype"]
            await message.reply_text("<b>Hello Dear \n\nYou Need To Join In My Channel To Use Me\n\nKindly Please Join Channel</b>",
                                     reply_to_message_id=message.id,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton("🔺 Update Channel 🔺", url=f"https://t.me/{update_channel}")]]))
            await client.send_message(log_channel,f"<b><u>New User Started The Bot</u></b> \n\n<b>User ID</b> : `{user_id}` \n<b>First Name</b> : {message.from_user.first_name} \n<b>Last Name</b> : {message.from_user.last_name} \n<b>User Name</b> : @{message.from_user.username} \n<b>User Mention</b> : {message.from_user.mention} \n<b>User Link</b> : <a href='tg://openmessage?user_id={user_id}'>Click Here</a> \n<b>User Plan</b> : {user}",
                                                                                                       reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔺  Rᴇsᴛʀɪᴄᴛ Usᴇʀ ( **PM** )  🔺", callback_data="ceasepower")]]))
            return
        
    bot_data = find_one(int(botid))
    prrename = bot_data['total_rename']
    prsize = bot_data['total_size']
    user_deta = find_one(user_id)

    if "date" in user_deta:
        used_date = user_deta["date"]
    else:
        await message.reply_text("There was an issue retrieving your data. Please try again later.")
        return

    buy_date = user_deta.get("prexdate")
    daily = user_deta.get("daily", 0)
    user_type = user_deta.get("usertype", "Free")

    c_time = time.time()

    LIMIT = 120 if user_type == "Free" else 10
    then = used_date + LIMIT
    left = round(then - c_time)
    conversion = datetime.timedelta(seconds=left)
    ltime = str(conversion)
    
    if left > 0:
        await message.reply_text(f"<b>Sorry Dude I Am Not Only For You \n\nFlood Control Is Active So Please Wait For {ltime} </b>", reply_to_message_id=message.id)
    else:
        media = await client.get_messages(message.chat.id, message.id)
        file = media.document or media.video or media.audio
        dcid = FileId.decode(file.file_id).dc_id
        filename = file.file_name
        file_id = file.file_id
        value = 2147483648
        used_ = find_one(message.from_user.id)
        used = used_.get("used_limit", 0)
        limit = used_.get("uploadlimit", value)
        expi = daily - int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
        
        if expi != 0:
            today = date_.today()
            pattern = '%Y-%m-%d'
            epcho = int(time.mktime(time.strptime(str(today), pattern)))
            daily(message.from_user.id, epcho)
            used_limit(message.from_user.id, 0)
        
        remain = limit - used
        if remain < int(file.file_size):
            await message.reply_text(f"100% Of Daily {humanbytes(limit)} Data Quota Exhausted.\n\n<b>File Size Detected :</b> {humanbytes(file.file_size)}\n<b>Used Daily Limit :</b> {humanbytes(used)}\n\nYou Have Only <b>{humanbytes(remain)}</b> Left On Your Account.\n\nIf U Want To Rename Large File Upgrade Your Plan", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Upgrade", callback_data="upgrade")]]))
            return
        
        if value < file.file_size:
            if STRING:
                if buy_date is None:
                    await message.reply_text(f"You Can't Upload More Than 2GB File\n\nYour Plan Doesn't Allow To Upload Files That Are Larger Than 2GB\n\nUpgrade Your Plan To Rename Files Larger Than 2GB", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Upgrade", callback_data="upgrade")]]))
                    return
                
                pre_check = check_expi(buy_date)
                if pre_check:
                    await message.reply_text(f"Your user plan has expired. Please upgrade your account to rename larger files.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Upgrade", callback_data="upgrade")]]))
                    return
                
                await message.reply_text("**Sorry! I cannot upload files larger than 2GB on Telegram at the moment.**")
                return
            else:
                if buy_date is None:
                    await message.reply_text(f"You Can't Upload More Than 2GB File\n\nYour Plan Doesn't Allow To Upload Files That Are Larger Than 2GB\n\nUpgrade Your Plan To Rename Files Larger Than 2GB", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Upgrade", callback_data="upgrade")]]))
                    return
