import os
import re
from pathlib import Path

# 📂 Paths
base_dir = Path(__file__).resolve().parent.parent  # From Scripts → VidHandler
txt_dir = base_dir / "Txt Files"

VID_FOLDER = Path(os.path.expanduser('~')) / 'Downloads' / 'Video'  # Resolves to C:\Users\YourUser\Downloads\Video
print(VID_FOLDER)
CHANNELS_FILE = txt_dir / "youtube_channels.txt"
ANIME_FILE = txt_dir / "anime_name.txt"

# 🔹 Load YouTube channel names from the file
def get_channel_mapping():
    channel_mapping = {}

    try:
        with CHANNELS_FILE.open("r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(" | ")
                if len(parts) == 2:
                    video_title, channel_name = parts
                    channel_mapping[clean_text(video_title)] = channel_name
                else:
                    print(f"⚠ Skipping invalid line: {line.strip()} (wrong format)")
    except FileNotFoundError:
        print(f"❌ ERROR: File {CHANNELS_FILE} not found!")

    print(f"✅ Loaded {len(channel_mapping)} entries from {CHANNELS_FILE}")
    return channel_mapping

# 🔹 Load Anime names from the file
def get_anime_mapping():
    anime_mapping = {}
    try:
        with ANIME_FILE.open("r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(" | ")
                if len(parts) == 2:
                    jp, en = parts
                    pattern = re.compile(re.escape(clean_text(jp)), re.IGNORECASE)
                    anime_mapping[pattern] = en
    except FileNotFoundError:
        print(f"❌ ERROR: File {ANIME_FILE} not found!")
    print(f"🎌 Loaded {len(anime_mapping)} anime entries from {ANIME_FILE}")
    return anime_mapping

# 🔹 Function to clean text
def clean_text(text):
    text = text.lower()
    text = text.replace("_", " ").replace("/", " ")
    text = text.replace(":", " ")
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# 🔹 Sanitize filenames for Windows compatibility
def sanitize_filename(name):
    name = name.replace(":", " ")
    return re.sub(r'[<>"/\\|?*]', '', name)

# 🔹 Rename video files with the correct channel name
def rename_videos():
    channel_mapping = get_channel_mapping()
    anime_mapping = get_anime_mapping()

    print(f"🔍 Scanning folder: {VID_FOLDER}")

    # 🔄 Rename normal videos
    print("🔄 Renaming normal videos...")
    for file in VID_FOLDER.iterdir():
        if not file.is_file():
            continue

        file_name = file.stem
        file_ext = file.suffix
        clean_name = clean_text(file_name)

        matched_channel = None
        for video_title, channel_name in channel_mapping.items():
            if video_title in clean_name:
                matched_channel = channel_name
                break

        if matched_channel:
            new_file_name = sanitize_filename(f"{matched_channel} - {file.name}")
            new_path = file.with_name(new_file_name)
            file.rename(new_path)
            print(f"✅ Renamed: {file.name} → {new_file_name}")
        else:
            print(f"⚠ No match found for: {file.name}")

    # 🔄 Rename anime videos
    print("🔄 Renaming anime videos...")
    for file in VID_FOLDER.iterdir():
        if not file.is_file():
            continue

        anime_found = False
        for pattern, en_name in anime_mapping.items():
            if pattern.search(clean_text(file.name)):
                new_base_name = pattern.sub(en_name, file.name)
                new_base_name = sanitize_filename(new_base_name)
                new_path = file.with_name(new_base_name)
                file.rename(new_path)
                print(f"🎌 Anime renamed: {file.name} → {new_base_name}")
                anime_found = True
                break

        if not anime_found:
            print(f"⚠ No anime match found for: {file.name}")

    # Clean up youtube_channels.txt (optional)
    CHANNELS_FILE.write_text("", encoding="utf-8")
    print("🧹 youtube_channels.txt cleared!")

# Run the script
if __name__ == "__main__":
    rename_videos()
