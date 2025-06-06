import subprocess
import sys
from pathlib import Path

def get_base_dir():
    if getattr(sys, 'frozen', False):
        # If running as an .exe, go up one level from dist to VidHandler
        return Path(sys.executable).resolve().parent.parent
    else:
        # If running as a script, get the script's own directory
        return Path(__file__).resolve().parent

base_dir = get_base_dir()
code_caller_path = base_dir / "Scripts" / "CodeCaller.py"

print(f"[DEBUG] CodeCaller path: {code_caller_path}")

def run_py_file():
    if not code_caller_path.exists():
        print(f"[ERROR] CodeCaller.py not found at: {code_caller_path}")
        input("Press Enter to exit...")
        return

    CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    subprocess.Popen(
        ["python", str(code_caller_path)],
        creationflags=CREATE_NO_WINDOW
    )

if __name__ == "__main__":
    run_py_file()
