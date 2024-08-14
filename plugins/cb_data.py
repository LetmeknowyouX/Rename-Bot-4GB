from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from PIL import Image
from helper.progress import progress_for_pyrogram
from helper.database import find_one, used_limit
from helper.thumbnail import take_screen_shot, fix_thumb
from helper.metadata import extractMetadata, createParser
from helper.utils import escape_invalid_curly_brackets
from config import LOG_CHANNEL
import os
import time
import random
from datetime import timedelta
from pyrogram.errors import RPCError

app = Client("my_bot")

@app.on_callback_query(filters.regex("file"))
async def file_rename(bot: Client, update: CallbackQuery):
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
    ms = await update.message.edit("`Trying To Download`")
    c_time = time.time()
    try:
        path = await bot.download_media(message=file, progress=progress_for_pyrogram, progress_args=("`Trying To Download....`", ms, c_time))
    except Exception as e:
        neg_used = used - int(file.file_size)
        used_limit(update.from_user.id, neg_used)
        await ms.edit(f"Error: {e}")
        return

    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)

    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds

    user_id = int(update.message.chat.id)
    data = find_one(user_id)
    c_caption = data.get(1, "")
    thumb = data.get(0)

    if c_caption:
        vid_list = ["filename", "filesize", "duration"]
        new_tex = escape_invalid_curly_brackets(c_caption, vid_list)
        caption = new_tex.format(filename=new_filename, filesize=humanbytes(file.file_size), duration=timedelta(seconds=duration))
    else:
        caption = f"**{new_filename}**"

    if thumb:
        ph_path = await bot.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
        c_time = time.time()
    else:
        try:
            ph_path_ = await take_screen_shot(file_path, os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
            width, height, ph_path = await fix_thumb(ph_path_)
        except Exception as e:
            ph_path = None
            print(e)

    value = 2090000000
    if value < file.file_size:
        await ms.edit("`Trying To Upload`")
        try:
            filw = await bot.send_video(LOG_CHANNEL, video=file_path, thumb=ph_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("`Trying To Uploading....`", ms, c_time))
            from_chat = filw.chat.id
            mg_id = filw.id
            time.sleep(2)
            await bot.copy_message(update.from_user.id, from_chat, mg_id)
            await ms.delete()
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
        except RPCError as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(f"Error: {e}")
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
    else:
        await ms.edit("`Trying To Upload`")
        c_time = time.time()
        try:
            await bot.send_video(update.from_user.id, video=file_path, thumb=ph_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("`Trying To Uploading....`", ms, c_time))
            await ms.delete()
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
        except RPCError as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(f"Error: {e}")
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)

@app.on_callback_query(filters.regex("aud"))
async def aud(bot: Client, update: CallbackQuery):
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
    ms = await update.message.edit("`Trying To Download`")
    c_time = time.time()
    try:
        path = await bot.download_media(message=file, progress=progress_for_pyrogram, progress_args=("`Trying To Download....`", ms, c_time))
    except Exception as e:
        neg_used = used - int(file.file_size)
        used_limit(update.from_user.id, neg_used)
        await ms.edit(f"Error: {e}")
        return

    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)

    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds

    user_id = int(update.message.chat.id)
    data = find_one(user_id)
    c_caption = data.get(1, "")
    thumb = data.get(0)

    if c_caption:
        aud_list = ["filename", "filesize", "duration"]
        new_tex = escape_invalid_curly_brackets(c_caption, aud_list)
        caption = new_tex.format(filename=new_filename, filesize=humanbytes(file.file_size), duration=timedelta(seconds=duration))
    else:
        caption = f"**{new_filename}**"

    if thumb:
        ph_path = await bot.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
        await ms.edit("`Trying To Upload`")
        c_time = time.time()
        try:
            await bot.send_audio(update.message.chat.id, audio=file_path, caption=caption, thumb=ph_path, duration=duration, progress=progress_for_pyrogram, progress_args=("`Trying To Uploading....`", ms, c_time))
            await ms.delete()
            os.remove(file_path)
            os.remove(ph_path)
        except RPCError as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(f"Error: {e}")
            os.remove(file_path)
            os.remove(ph_path)
    else:
        await ms.edit("`Trying To Upload`")
        c_time = time.time()
        try:
            await bot.send_audio(update.message.chat.id, audio=file_path, caption=caption, duration=duration, progress=progress_for_pyrogram, progress_args=("`Trying To Uploading....`", ms, c_time))
            await ms.delete()
            os.remove(file_path)
        except RPCError as e:
            await ms.edit(f"Error: {e}")
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            os.remove(file_path)

if __name__ == "__main__":
    app.run()
