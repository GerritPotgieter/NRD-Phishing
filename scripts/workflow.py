import subprocess
import os
from pathlib import Path 
from parse import main as parse_main               # Your daily file parser script
from parse_full import main as parse_full_main     # Your full combined file parser script
from junk_dump import main as junk_dump_main       # Your junk filter script
from domain_profiler import main as profiler_main  # Your domain enrichment script
from scan import main as scan_main                   # Your domain scanning script


def run_downloader(day_range=5):
   import subprocess
from pathlib import Path

def run_downloader(day_range=5):

    script_path = Path(__file__).parent / "nrd-list-downloader.sh"
    win_path = script_path.resolve()

    drive_letter = win_path.drive[0].lower()
    # Use as_posix to get forward slashes and remove the drive letter + colon (e.g., C:)
    wsl_script_path = f"/mnt/{drive_letter}{win_path.as_posix()[2:]}"
    wsl_dir_path = str(Path(wsl_script_path).parent)

    # Use double quotes for cd path and script path in bash command to handle spaces
    cmd = f'cd "{wsl_dir_path}" && DAY_RANGE={day_range} "{wsl_script_path}"'
    print(f"[*] Running downloader: {cmd}")

    subprocess.run(["bash", "-c", cmd], check=True)




def main():
    DAY_RANGE = 5

    # Step 1 - Download domain lists
    #run_downloader(day_range=5)

    # Step 2 - Parse individual daily files
    parse_main()

    # Step 2.5 - Optional: Parse the full combined NRD list
    #combined_filename = f"nrd-{DAY_RANGE}days-free.txt"
    #parse_full_main(combined_filename)

    # Step 3 - Filter junk and reduce noise
    junk_dump_main()

    # Step 4 - Enrich domain data (optional)
    # profiler_main("example.com")

    #Step 5 - scan recent domains and check for changed hashes
    scan_main()


if __name__ == "__main__":
    main()
