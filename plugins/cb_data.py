from pyrogram import Client, filters
from plugins.thumbfunction import take_screen_shot, fix_thumb
from helper.database import find, find_one, used_limit, addthumb, delthumb
import os
import time
import random
from PIL import Image
from datetime import timedelta

token = "YOUR_BOT_TOKEN_HERE"  # Replace with your actual bot token
app = Client("my_bot", bot_token=token)

@app.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    await message.reply_text("Welcome! Send me a file and I'll process it.")

@app.on_message(filters.private & filters.command(['viewthumb']))
async def viewthumb(client, message):
    thumb = find(int(message.chat.id))[0]
    if thumb:
        await client.send_photo(message.chat.id, photo=f"{thumb}")
    else:
        await message.reply_text("**You Don't Have Any Thumbnail ❌**")

@app.on_message(filters.private & filters.command(['delthumb']))
async def removethumb(client, message):
    delthumb(int(message.chat.id))
    await message.reply_text("**Thumbnail Deleted Successfully 🗑️**")

@app.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    file_id = str(message.photo.file_id)
    addthumb(message.chat.id, file_id)
    await message.reply_text("**Thumbnail Saved Successfully ✅**")

@app.on_message(filters.private & filters.document)
async def handle_document(client, message):
    # Process the received document if needed
    pass

@app.on_callback_query(filters.regex("vid"))
async def vid(client, update):
    new_name = update.message.text
    used_ = find_one(update.from_user.id)
    used = used_["used_limit"]
    name = new_name.split(":-")
    new_filename = name[1]
    file_path = f"downloads/{new_filename}"
    message = update.message.reply_to_message
    file = message.document or message.video or message.audio
    ms = await update.message.edit("`Tʀyɪɴɢ Tᴏ Dᴏᴡɴʟᴏᴀᴅ`")
    used_limit(update.from_user.id, file.file_size)
    c_time = time.time()
    total_used = used + int(file.file_size)
    used_limit(update.from_user.id, total_used)
    try:
        path = await client.download_media(message=file, progress=progress_for_pyrogram, progress_args=("`Tʀyɪɴɢ Tᴏ Dᴏᴡɴʟᴏᴀᴅɪɴɢ....`", ms, c_time))
    except Exception as e:
        neg_used = used - int(file.file_size)
        used_limit(update.from_user.id, neg_used)
        await ms.edit(str(e))
        return

    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    user_id = int(update.message.chat.id)
    data = find(user_id)
    c_caption = data[1] if len(data) > 1 else None
    thumb = data[0]

    duration = 0  # Default duration
    caption = c_caption.format(filename=new_filename, filesize=humanbytes(file.file_size), duration=timedelta(seconds=duration)) if c_caption else f"**{new_filename}**"

    if thumb:
        ph_path = await client.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320)).save(ph_path, "JPEG")
    else:
        try:
            ph_path_ = await take_screen_shot(file_path, os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
            width, height, ph_path = await fix_thumb(ph_path_)
        except Exception as e:
            ph_path = None
            print(e)

    value = 2090000000
    if value < file.file_size:
        await ms.edit("`Tʀyɪɴɢ Tᴏ Uᴘʟᴏᴀᴅ`")
        try:
            filw = await client.send_video(log_channel, video=file_path, thumb=ph_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("`Tʀyɪɴɢ Tᴏ Uᴘʟᴏᴀᴅɪɴɢ....`", ms, c_time))
            from_chat = filw.chat.id
            mg_id = filw.id
            time.sleep(2)
            await client.copy_message(update.from_user.id, from_chat, mg_id)
            await ms.delete()
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(str(e))
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
    else:
        await ms.edit("`Tʀyɪɴɢ Tᴏ Uᴘʟᴏᴀᴅ`")
        c_time = time.time()
        try:
            await client.send_video(update.from_user.id, video=file_path, thumb=ph_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("`Tʀyɪɴɢ Tᴏ Uᴘʟᴏᴀᴅɪɴɢ....`", ms, c_time))
            await ms.delete()
            os.remove(file_path)
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(str(e))
            os.remove(file_path)

@app.on_callback_query(filters.regex("aud"))
async def aud(client, update):
    new_name = update.message.text
    used_ = find_one(update.from_user.id)
    used = used_["used_limit"]
    name = new_name.split(":-")
    new_filename = name[1]
    file_path = f"downloads/{new_filename}"
    message = update.message.reply_to_message
    file = message.document or message.video or message.audio
    total_used = used + int(file.file_size)
    used_limit(update.from_user.id, total_used)
    ms = await update.message.edit("`Tʀyɪɴɢ Tᴏ Dᴏᴡɴʟᴏᴀᴅ`")
    c_time = time.time()
    try:
        path = await client.download_media(message=file, progress=progress_for_pyrogram, progress_args=("`Tʀyɪɴɢ Tᴏ Dᴏᴡɴʟᴏᴀᴅɪɴɢ....`", ms, c_time))
    except Exception as e:
        neg_used = used - int(file.file_size)
        used_limit(update.from_user.id, neg_used)
        await ms.edit(str(e))
        return

    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    duration = 0  # Default duration
    user_id = int(update.message.chat.id)
    data = find(user_id)
    c_caption = data[1] if len(data) > 1 else None
    thumb = data[0]
    caption = c_caption.format(filename=new_filename, filesize=humanbytes(file.file_size), duration=timedelta(seconds=duration)) if c_caption else f"**{new_filename}**"

    if thumb:
        ph_path = await client.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320)).save(ph_path, "JPEG")
    else:
        ph_path = None  # No thumbnail handling

    await ms.edit("`Tʀyɪɴɢ Tᴏ Uᴘʟᴏᴀᴅ`")
    c_time = time.time()
    try:
        await client.send_audio(update.from_user.id, audio=file_path, thumb=ph_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("`Tʀyɪɴɢ Tᴏ Uᴘʟᴏᴀᴅɪɴɢ....`", ms, c_time))
        await ms.delete()
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
    except Exception as e:
        neg_used = used - int(file.file_size)
        used_limit(update.from_user.id, neg_used)
        await ms.edit(str(e))
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)

app.run()
