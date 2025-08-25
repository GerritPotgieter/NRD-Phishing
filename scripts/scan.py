import requests
import hashlib
import csv
import time
from datetime import datetime
import os

# Default paths
INPUT_FILE = "Output/Full_Cleaned_Report/total_filtered_domains.txt"
OUTPUT_CSV = "Output/Domain_Activity_Log.csv"

# Function to fetch domain content and compute hash
def fetch_domain_hash(domain, timeout=5):
    for url in [f"https://{domain}", f"http://{domain}"]:
        try:
            r = requests.get(url, timeout=timeout)
            if r.status_code == 200 and r.text.strip():
                return True, hashlib.md5(r.text.encode("utf-8")).hexdigest()
        except requests.RequestException:
            continue
    return False, None

def main(input_file: str = INPUT_FILE, output_csv: str = OUTPUT_CSV, timeout: int = 5, delay: float = 0.5) -> None:
    """Run the domain activity scan end-to-end.

    Args:
        input_file: Path to file with one domain per line.
        output_csv: Path to write/update the activity log CSV.
        timeout: Per-request timeout in seconds.
        delay: Sleep between domain checks to avoid hammering servers.
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Load domains
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        domains = [line.strip() for line in f if line.strip()]

    # Load existing CSV data if exists (to detect content changes)
    domain_data = {}
    if os.path.exists(output_csv):
        with open(output_csv, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                domain_data[row["domain"]] = row

    # Prepare CSV header
    fieldnames = ["domain", "last_checked", "is_active", "content_hash", "content_changed"]

    # Open CSV for writing (overwrite each run)
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for domain in domains:
            is_active, content_hash = fetch_domain_hash(domain, timeout=timeout)
            prev_hash = domain_data.get(domain, {}).get("content_hash")
            changed = bool(content_hash and prev_hash != content_hash)

            writer.writerow({
                "domain": domain,
                "last_checked": datetime.utcnow().isoformat(),
                "is_active": is_active,
                "content_hash": content_hash or "",
                "content_changed": changed,
            })

            status = "[ACTIVE]" if is_active else "[INACTIVE]"
            print(f"{status} {domain} | Hash changed: {changed}")
            time.sleep(delay)  # avoid overloading servers


if __name__ == "__main__":
    main()
