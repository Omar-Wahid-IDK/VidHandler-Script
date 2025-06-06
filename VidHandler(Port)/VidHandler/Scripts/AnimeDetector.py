import os
import re
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent  # From Scripts → VidHandler
txt_dir = base_dir / "Txt Files"

video_folder = os.path.expanduser('~') + r'\Downloads\Video'
anime_detect_path = txt_dir / "anime_detect.txt"
anime_names_path = txt_dir / "anime_names.txt"

def clean_string(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def extract_season_ep(filename):
    season = ''
    episode = ''

    # Season patterns (S1, Season 1, or just s1)
    season_match = re.search(r'(?:S|Season)[ _\-]?(\d{1,2})', filename, re.IGNORECASE)
    if not season_match:
        season_match = re.search(r'\bs(\d{1,2})\b', filename, re.IGNORECASE)
    if season_match:
        season = season_match.group(1)

    # Episode patterns: S1E03, Ep03, Episode 03, _03_, -03-, .03.
    episode_match = re.search(
        r'(?:S\d+)?E(\d{1,3})|(?:Ep|Episode)[ _\-]?(\d{1,3})|[_\-\s\.](\d{1,3})(?=[_\-\s\.])',
        filename,
        re.IGNORECASE
    )
    if episode_match:
        episode = next(g for g in episode_match.groups() if g)

    return season, episode

# Load anime names for detection
try:
    with open(anime_detect_path, 'r', encoding='utf-8') as file:
        anime_detect_list = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print(f"❌ File not found: {anime_detect_path}")
    exit()

# Load anime English names mapping with cleaned keys
anime_english_map = {}
try:
    with open(anime_names_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if '=' in line:
                jp, en = line.split('=', 1)
                jp_clean = clean_string(jp.strip())
                anime_english_map[jp_clean] = en.strip()
except FileNotFoundError:
    print(f"❌ File not found: {anime_names_path}")
    exit()

print(f"✅ Loaded {len(anime_detect_list)} anime names for detection.")
print(f"✅ Loaded {len(anime_english_map)} English name mappings.")

video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm', '.ts'}

try:
    files = os.listdir(video_folder)
except FileNotFoundError:
    print(f"❌ Folder not found: {video_folder}")
    exit()

print(f"📂 Found {len(files)} files in folder.")

found_any = False
for filename in files:
    file_path = os.path.join(video_folder, filename)
    if os.path.isfile(file_path):
        name, ext = os.path.splitext(filename)
        if ext.lower() in video_extensions:
            cleaned_filename = clean_string(name)
            for anime_jp in anime_detect_list:
                cleaned_anime = clean_string(anime_jp)
                if cleaned_anime in cleaned_filename:
                    # Determine the display name (English or original)
                    display_name = anime_english_map.get(cleaned_anime, anime_jp)

                    # Extract season and episode
                    season, episode = extract_season_ep(filename)

                    # Build new filename parts with no leading zeros
                    parts = ['[AH]']
                    parts.append(display_name)
                    parts.append('(1080p)')  # Always add (1080p)

                    if season and episode:
                        parts.append(f'S{int(season)}E{int(episode)}')
                    elif episode:
                        parts.append(f'E{int(episode)}')

                    new_name = ' '.join(parts) + ext.lower()
                    new_path = os.path.join(video_folder, new_name)

                    # Avoid overwriting existing files
                    if os.path.exists(new_path):
                        print(f"⚠️ Skipping rename, target file exists: {new_name}")
                    else:
                        print(f"🔄 Renaming:\n  From: {filename}\n  To:   {new_name}")
                        os.rename(file_path, new_path)

                    found_any = True
                    break

if not found_any:
    print("🚫 No anime videos found.")
