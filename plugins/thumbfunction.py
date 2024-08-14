from PIL import Image
import os
import random
import io
import subprocess
import ffmpeg

async def take_screen_shot(video_path, output_dir, timestamp):
    output_path = os.path.join(output_dir, f"thumbnail_{timestamp}.jpg")
    command = (
        ffmpeg
        .input(video_path, ss=timestamp)
        .output(output_path, vframes=1)
        .run(capture_stdout=True, capture_stderr=True)
    )
    return output_path

async def fix_thumb(thumb_path):
    img = Image.open(thumb_path)
    img = img.convert("RGB")
    img = img.resize((320, 320))
    new_thumb_path = thumb_path.replace('.jpg', '_fixed.jpg')
    img.save(new_thumb_path, "JPEG")
    return img.size, new_thumb_path

def humanbytes(byte_size):
    """Convert bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if byte_size < 1024:
            return f"{byte_size:.2f} {unit}"
        byte_size /= 1024

def timedelta(seconds):
    """Convert seconds to a readable time format."""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02}:{int(m):02}:{int(s):02}"
