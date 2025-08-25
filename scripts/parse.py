import os
import re

# === Path Setup ===
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
input_dir = os.path.join(root_dir,"scripts" ,"daily", "free")
output_dir = os.path.join(root_dir, "Output", "ByDate")
os.makedirs(output_dir, exist_ok=True)

# === Static Regexes ===
pattern_coza = re.compile(r"\.co\.za$", re.IGNORECASE)
pattern_africa = re.compile(r"\.africa$", re.IGNORECASE)
pattern_absa = re.compile(r"absa", re.IGNORECASE)

# === Load Patterns per Category ===
def load_patterns(file_path):
    patterns = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                patterns.append(re.compile(re.escape(line), re.IGNORECASE))
    return patterns

typo_patterns = load_patterns(os.path.join(root_dir, "Patterns", "typos.txt"))
presuf_patterns = load_patterns(os.path.join(root_dir, "Patterns", "presuf.txt"))
tld_patterns = load_patterns(os.path.join(root_dir, "Patterns", "TLD.txt"))
keyword_patterns = load_patterns(os.path.join(root_dir, "Patterns", "keywords.txt"))

def parse_file(file_path, filename):
    # === Output Containers ===
    coza_only = []
    africa_only = []
    absa_only = []
    golden_matches = []
    typo_matches = []
    presuf_matches = []
    tld_matches = []
    keyword_matches = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
        for line in infile:
            domain = line.strip()
            if not domain:
                continue

            has_coza = bool(pattern_coza.search(domain))
            has_africa = bool(pattern_africa.search(domain))
            has_absa = bool(pattern_absa.search(domain))

            # Check pattern matches
            is_typo = any(p.search(domain) for p in typo_patterns)
            is_presuf = any(p.search(domain) for p in presuf_patterns)
            is_tld = any(p.search(domain) for p in tld_patterns)
            is_keyword = any(p.search(domain) for p in keyword_patterns)

            # === Categorization Logic ===
            if (has_coza or has_africa) and has_absa:
                golden_matches.append(domain)
            elif has_coza:
                coza_only.append(domain)
            elif has_absa:
                absa_only.append(domain)
            elif has_africa:
                africa_only.append(domain)

            # Permutation Matches
            if is_typo:
                typo_matches.append(domain)
            if is_presuf:
                presuf_matches.append(domain)
            if is_tld:
                tld_matches.append(domain)
            if is_keyword:
                keyword_matches.append(domain)

            

    # === Output File Writing ===
    output_path = os.path.join(output_dir, filename)
    with open(output_path, "w", encoding="utf-8") as outfile:
        # --- Summary Header ---
        outfile.write(f"Summary for {filename}:\n")
        outfile.write(f"  - Golden Matches     : {len(golden_matches)}\n")
        outfile.write(f"  - .co.za Only        : {len(coza_only)}\n")
        outfile.write(f"  - absa Only          : {len(absa_only)}\n")
        outfile.write(f"  - Typo Matches       : {len(typo_matches)}\n")
        outfile.write(f"  - Prefix/Suffix Hits : {len(presuf_matches)}\n")
        outfile.write(f"  - TLD Spoof Matches  : {len(tld_matches)}\n")
        outfile.write(f"  - Keyword Matches    : {len(keyword_matches)}\n")
        outfile.write(f"  - .africa Only       : {len(africa_only)}\n")
        outfile.write("=" * 40 + "\n\n")

        # --- Detailed Sections ---
        outfile.write("=== Golden Matches ===\n")
        outfile.writelines(f"{d}\n" for d in golden_matches)

        outfile.write("\n=== .co.za Only Matches ===\n")
        outfile.writelines(f"{d}\n" for d in coza_only)

        outfile.write("\n=== absa Only Matches ===\n")
        outfile.writelines(f"{d}\n" for d in absa_only)

        outfile.write("\n=== Typo Matches ===\n")
        outfile.writelines(f"{d}\n" for d in typo_matches)

        outfile.write("\n=== Prefix/Suffix Matches ===\n")
        outfile.writelines(f"{d}\n" for d in presuf_matches)

        outfile.write("\n=== TLD Matches ===\n")
        outfile.writelines(f"{d}\n" for d in tld_matches)

        outfile.write("\n=== Keyword Matches ===\n")
        outfile.writelines(f"{d}\n" for d in keyword_matches)

        outfile.write("\n=== .africa Only Matches ===\n")
        outfile.writelines(f"{d}\n" for d in africa_only)

    # === Print to Terminal ===
    print(f"[✓] {filename} → {output_path}")
    print(f"    - Golden Matches     : {len(golden_matches)}")
    print(f"    - .co.za Only        : {len(coza_only)}")
    print(f"    - absa Only          : {len(absa_only)}")
    print(f"    - Typo Matches       : {len(typo_matches)}")
    print(f"    - Prefix/Suffix Hits : {len(presuf_matches)}")
    print(f"    - TLD Spoof Matches  : {len(tld_matches)}")
    print(f"    - .africa Only       : {len(africa_only)}\n")

def main():
    if not os.path.exists(input_dir):
        print(f"[!] Input directory not found: {input_dir}")
        return

    for filename in sorted(os.listdir(input_dir)):
        file_path = os.path.join(input_dir, filename)

        if not os.path.isfile(file_path):
            continue

        output_file_path = os.path.join(output_dir, filename)
        if os.path.exists(output_file_path):
            print(f"[⏩] Skipping already parsed file: {filename}")
            continue

        parse_file(file_path, filename)

if __name__ == "__main__":
    main()
