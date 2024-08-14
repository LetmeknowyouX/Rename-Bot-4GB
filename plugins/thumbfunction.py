from pyrogram import Client, filters
from helper.database import find, delthumb, addthumb

@Client.on_message(filters.private & filters.command(['viewthumb']))
async def viewthumb(client, message):
    try:
        chat_id = int(message.chat.id)
        thumb = find(chat_id)[0]  # Ensure 'find' returns expected result
        if thumb:
            await client.send_photo(chat_id, photo=thumb)
        else:
            await message.reply_text("**You Don't Have Any Thumbnail ❌**")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@Client.on_message(filters.private & filters.command(['delthumb']))
async def removethumb(client, message):
    try:
        chat_id = int(message.chat.id)
        delthumb(chat_id)
        await message.reply_text("**Thumbnail Deleted Successfully 🗑️**")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@Client.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    try:
        file_id = str(message.photo.file_id)
        chat_id = int(message.chat.id)
        addthumb(chat_id, file_id)
        await message.reply_text("**Thumbnail Saved Successfully ✅**")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
