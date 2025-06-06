from pathlib import Path
import subprocess

# You're already in Scripts, so no need to add "Scripts" again
scripts_dir = Path(__file__).resolve().parent

# Directly define script paths
GetChannelName = scripts_dir / "GetChannelName.py"
VidRenamer = scripts_dir / "NewRenamer.py"
CheckVidOpp = scripts_dir / "CheckVidOpp.py"
sort_videos = scripts_dir / "NewSort.py"
CheckVid = scripts_dir / "CheckVid.py"
IconGetter = scripts_dir / "IconGetter.py"
IconAssinger = scripts_dir / "IconAssinger.py"
CricledImages = scripts_dir / "CircledImages.py"
IcoConverter = scripts_dir / "IcoConverter.py"
AnimeDetector = scripts_dir / "AnimeDetector.py"

def runpyfile():
    scripts = [
        GetChannelName,
        VidRenamer,
        CheckVidOpp,
        AnimeDetector,
        sort_videos,
        IconGetter,
        CricledImages,
        IcoConverter,
        IconAssinger,
        CheckVid
    ]

    for script in scripts:
        subprocess.run(["python", str(script)], creationflags=subprocess.CREATE_NO_WINDOW)

if __name__ == "__main__":
    runpyfile()
