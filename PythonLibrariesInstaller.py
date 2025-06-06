import importlib.util
import subprocess
import sys

# Mapping: pip name -> import name
required_packages = {
    "Pillow": "PIL",
    "requests": "requests",
    "yt_dlp": "yt_dlp",
    "beautifulsoup4": "bs4"
}

def is_installed(import_name):
    return importlib.util.find_spec(import_name) is not None

def install(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

print("Checking and installing missing packages...\n")

for pip_name, import_name in required_packages.items():
    if not is_installed(import_name):
        print(f"'{import_name}' not found. Installing '{pip_name}'...")
        install(pip_name)
    else:
        print(f"'{import_name}' is already installed.")

print("\nAll required packages are now installed.")
