import re
import os
from parse import load_patterns

# Load patterns from an external file
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IGNORE_FILE = os.path.join(root_dir, "Whitelist", "IgnoreDomains.txt")
INCLUDE_FILE = os.path.join(root_dir, "Whitelist", "IncludedHits.txt")
presuf_patterns = load_patterns(os.path.join(root_dir, "Patterns", "presuf.txt"))
tld_patterns = load_patterns(os.path.join(root_dir, "Patterns", "TLD.txt"))
keyword_patterns = load_patterns(os.path.join(root_dir, "Patterns", "keywords.txt"))

# stricter regex rules
strict_patterns = [
    re.compile(r"^absa.*", re.IGNORECASE),     # starts with absa
    re.compile(r".*absa$", re.IGNORECASE),     # ends with absa
    #re.compile(r"^absa.*absa$", re.IGNORECASE) # starts and ends with absa
    *presuf_patterns,
    *tld_patterns,
    *keyword_patterns
]

total_domains = []

def _normalize_domain(d: str) -> str:
    d = d.strip().lower()
    # Strip protocol if present and anything after a slash
    if "://" in d:
        d = d.split("://", 1)[1]
    if "/" in d:
        d = d.split("/", 1)[0]
    if d.startswith("www."):
        d = d[4:]
    return d.rstrip('.')

def _load_ignore_set(path: str) -> set[str]:
    ignore = set()
    if not os.path.exists(path):
        return ignore
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            ignore.add(_normalize_domain(line))
    return ignore

def _load_include_set(path: str) -> set[str]:
    include = set()
    if not os.path.exists(path):
        return include
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            include.add(_normalize_domain(line))
    return include

def filter_domains(domains, ignore_set: set[str]):
    filtered = []
    for domain in domains:
        norm = _normalize_domain(domain)
        if norm in ignore_set:
            continue
        if any(pat.match(domain) for pat in strict_patterns):
            filtered.append(domain)
    return filtered

def process_bydate_folder(input_folder, output_folder, ignore_set: set[str], include_set: set[str]):
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(os.path.join(root_dir, "Output", "Full_Cleaned_Report"), exist_ok=True)
    
    for filename in os.listdir(input_folder):
            with open(os.path.join(input_folder, filename), "r", encoding="utf-8") as f:
                domains = [line.strip() for line in f if line.strip()]

            cleaned = filter_domains(domains, ignore_set)
            total_domains.extend(cleaned)
            

            #if total finds is 0 then skip writing to file
            if not cleaned:
                print(f"[-] No valid domains found in {filename}, skipping.")
                continue
            output_file = os.path.join(output_folder, filename)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(cleaned))
            
            print(f"[+] Processed {filename}: {len(cleaned)} kept out of {len(domains)}")
            #write the total domains to a file

    # Merge include_set once and de-duplicate while preserving order
    merged = list(dict.fromkeys(total_domains + list(include_set)))
    total_output_file = os.path.join("Output/Full_Cleaned_Report", "total_filtered_domains.txt")
    with open(total_output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(merged))
    print(f"[+] Total filtered domains written to {total_output_file}")


def main():
    input_folder = "Output/ByDate"
    output_folder = "Output/ByDate_Clean"
    
    print("[*] Starting domain filtering process...")
    ignore_set = _load_ignore_set(IGNORE_FILE)
    if ignore_set:
        print(f"[i] Loaded {len(ignore_set)} ignored domain(s) from Whitelist/IgnoreDomains.txt")
    else:
        print("[i] No ignore list entries found or file missing; proceeding without exclusions")

    include_set = _load_include_set(INCLUDE_FILE)
    if include_set:
        print(f"[i] Loaded {len(include_set)} included domain(s) from Whitelist/IncludedHits.txt")
    else:
        print("[i] No include list entries found or file missing; proceeding without inclusions")

    process_bydate_folder(input_folder, output_folder, ignore_set, include_set)
    print("[✓] Domain filtering complete. Check Output/Full_Cleaned_Report for total filtered domains.")

if __name__ == "__main__":
    main()
