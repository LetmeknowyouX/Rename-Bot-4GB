from PIL import Image
import os
import ffmpeg
from PIL import Image

# Set the path to the ffmpeg executable
FFMPEG_PATH = '/path/to/your/helper/folder/ffmpeg'  # Update this path

def take_screen_shot(file_path, output_folder, timestamp):
    try:
        output_file = os.path.join(output_folder, 'screenshot.jpg')
        (
            ffmpeg
            .input(file_path, ss=timestamp)
            .output(output_file, vframes=1)
            .run(cmd=FFMPEG_PATH)
        )
        return output_file
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None

def fix_thumb(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        img = img.resize((320, 320))
        thumb_path = image_path.replace(".jpg", "_thumb.jpg")
        img.save(thumb_path, "JPEG")
        return thumb_path
    except Exception as e:
        print(f"Error fixing thumbnail: {e}")
        return None
