import os
import shutil

# Define the parent folder
script_dir = os.path.dirname(__file__)  # Get the directory where the script is located
config_path = os.path.join(script_dir, '..', '..', 'Paths.txt')  # Navigate to E:\Projects\VidHandler(Port)\Paths.txt

# Read the Paths.txt file to load YouTube and Anime folder paths
if os.path.exists(config_path):
    with open(config_path, 'r') as file:
        lines = file.readlines()
        Youtube_folder = lines[0].strip()  # Assuming the first line contains the YouTube folder path
else:
    print("No Folder Paths Known")

# Define common video file extensions
video_extensions = {".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm"}

# Iterate through subfolders in the parent directory
for folder in os.listdir(Youtube_folder):
    folder_path = os.path.join(Youtube_folder, folder)

    # Check if it's a folder
    if os.path.isdir(folder_path):
        # Check for video files inside the folder
        contains_videos = any(
            file.lower().endswith(tuple(video_extensions))
            for file in os.listdir(folder_path)
        )

        # Append check mark if videos are found and it's not already marked
        if contains_videos and "✔" not in folder:
            new_folder_name = f"{folder} ✔"
            new_folder_path = os.path.join(Youtube_folder, new_folder_name)
            shutil.move(folder_path, new_folder_path)
            print(f"Marked: {new_folder_name}")

        # Remove check mark if no videos are found
        elif not contains_videos and "✔" in folder:
            new_folder_name = folder.replace(" ✔", "")
            new_folder_path = os.path.join(Youtube_folder, new_folder_name)
            shutil.move(folder_path, new_folder_path)
            print(f"Unmarked: {new_folder_name}")