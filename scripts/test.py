import requests
import csv
import re
import socket
from datetime import datetime
from pathlib import Path

# Config
PATTERNS_DIR = Path("./Patterns")  # adjust if needed
CSV_OUTPUT = "ct_results.csv"
TXT_OUTPUT = "ct_domains.txt"
CTLOG_URL = "https://crt.sh/?q=%25.{}&output=json"  # %25 = URL encoded %

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

def fetch_ct_logs(keyword):
    try:
        resp = requests.get(CTLOG_URL.format(keyword), timeout=20)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[!] Error fetching CT logs for {keyword}: {e}")
        return []

def extract_domains(entry):
    names = entry.get("name_value", "").split("\n")
    return [n.strip().lower() for n in names if re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", n)]

def main():
    keywords = load_all_patterns()
    print(f"[*] Loaded {len(keywords)} unique patterns")
    
    seen_domains = set()
    results = []

    for kw in keywords:
        print(f"[*] Searching CT logs for: {kw}")
        entries = fetch_ct_logs(kw)
        for e in entries:
            for d in extract_domains(e):
                if d not in seen_domains:
                    seen_domains.add(d)
                    active = dns_active(d)
                    results.append({
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "domain": d,
                        "matched_variant": kw,
                        "dns_active": active,
                        "source": "CT"
                    })

    # Save CSV (full details)
    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "domain", "matched_variant", "dns_active", "source"])
        writer.writeheader()
        writer.writerows(results)

    # Save TXT (just domains)
    with open(TXT_OUTPUT, "w", encoding="utf-8") as f:
        for r in results:
            f.write(r["domain"] + "\n")

    print(f"[+] Saved {len(results)} results to {CSV_OUTPUT} and {TXT_OUTPUT}")

if __name__ == "__main__":
    main()
