import certstream
import csv
import re
import socket
from datetime import datetime
from pathlib import Path

# Config
PATTERNS_DIR = Path("./Patterns")  # adjust if needed
CSV_OUTPUT = "ct_results.csv"
TXT_OUTPUT = "ct_domains.txt"

PATTERN_FILES = [
    "keywords.txt",
    "presuf.txt",
    "TLD.txt",
    "typos.txt"
]

def load_all_patterns():
    patterns = set()
    for filename in PATTERN_FILES:
        file_path = PATTERNS_DIR / filename
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    kw = line.strip().lower()
                    if kw and not kw.startswith("#"):
                        patterns.add(kw)
        else:
            print(f"[!] Pattern file missing: {file_path}")
    return sorted(patterns)

def dns_active(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False

def process_cert(message, patterns, writer, txt_file, seen_domains):
    if message["message_type"] != "certificate_update":
        return
    
    all_domains = message["data"]["leaf_cert"]["all_domains"]
    for d in all_domains:
        d = d.lower()
        if d not in seen_domains and any(p in d for p in patterns):
            seen_domains.add(d)
            active = dns_active(d)
            row = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "domain": d,
                "dns_active": active,
                "source": "CertStream"
            }
            writer.writerow(row)
            txt_file.write(d + "\n")
            txt_file.flush()
            print(f"[+] Match: {d} (active={active})")

def main():
    patterns = load_all_patterns()
    print(f"[*] Loaded {len(patterns)} unique patterns")

    seen_domains = set()

    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as f_csv, \
         open(TXT_OUTPUT, "w", encoding="utf-8") as f_txt:

        fieldnames = ["timestamp", "domain", "dns_active", "source"]
        writer = csv.DictWriter(f_csv, fieldnames=fieldnames)
        writer.writeheader()

        print("[*] Connecting to CertStream...")
        certstream.listen_for_events(
            lambda m, _: process_cert(m, patterns, writer, f_txt, seen_domains),
            url="wss://certstream.calidog.io/"
        )

if __name__ == "__main__":
    main()
