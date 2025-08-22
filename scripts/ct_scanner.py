import json
import re
from pathlib import Path
from datetime import datetime
import sys

# Config
PATTERNS_DIR = Path("./Patterns")  # relative to Scripts/
RAW_JSONL = Path("./Output/Gungnir_Reports/all.jsonl")
FILTERED_JSONL = Path("./Output/Gungnir_Reports/filtered.jsonl")
FILTERED_TXT = Path("./Output/Gungnir_Reports/filtered.txt")

PATTERN_FILES = [
    "keywords.txt",
    "presuf.txt",
    "TLD.txt",
    "typos.txt"
]

def load_patterns():
    patterns = set()
    for fname in PATTERN_FILES:
        fpath = PATTERNS_DIR / fname
        if fpath.exists():
            with open(fpath, "r", encoding="utf-8") as f:
                for line in f:
                    kw = line.strip().lower()
                    if kw and not kw.startswith("#"):
                        patterns.add(re.escape(kw))  # escape for regex safety
        else:
            print(f"[!] Missing pattern file: {fpath}")
    return list(patterns)

def main():
    patterns = load_patterns()
    if not patterns:
        print("[!] No patterns loaded, exiting.")
        return

    regex = re.compile(r"(" + "|".join(patterns) + r")", re.IGNORECASE)

    hits = []
    with open(FILTERED_JSONL, "a", encoding="utf-8-sig", errors="ignore") as outfile:
        for line in sys.stdin:
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            domain = obj.get("common_name", "")
            dns_names = obj.get("dns_names", [])
            all_names = [domain] + dns_names

            if any(regex.search(name) for name in all_names):
                obj["matched_at"] = datetime.utcnow().isoformat() + "Z"
                outfile.write(json.dumps(obj) + "\n")
                hits.append(domain)

    print(f"[+] Found {len(hits)} hits. Saved to {FILTERED_JSONL} and {FILTERED_TXT}")

if __name__ == "__main__":
    main()
