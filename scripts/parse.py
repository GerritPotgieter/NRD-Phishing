import os
import re

# Define paths
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
input_dir = os.path.join(root_dir, "daily", "free")
output_dir = os.path.join(root_dir, "Output", "ByDate")
os.makedirs(output_dir, exist_ok=True)

# Define regex patterns
pattern_coza = re.compile(r"\.co\.za$", re.IGNORECASE)
pattern_africa = re.compile(r"\.africa$", re.IGNORECASE)
pattern_absa = re.compile(r"absa", re.IGNORECASE)
pattern_aabsa = re.compile(r"aabsa", re.IGNORECASE)
pattern_abbsa = re.compile(r"abbsa", re.IGNORECASE)
pattern_abssa = re.compile(r"abssa", re.IGNORECASE)
pattern_absaa = re.compile(r"absaa", re.IGNORECASE)

def parse_file(file_path, filename):
    coza_only = []
    africa_only = []
    absa_only = []
    absa_typo_only = []
    golden_matches = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
        for line in infile:
            domain = line.strip()
            if not domain:
                continue

            has_coza = bool(pattern_coza.search(domain))
            has_africa = bool(pattern_africa.search(domain))
            has_absa = bool(pattern_absa.search(domain))
            has_aabsa = bool(pattern_aabsa.search(domain))
            has_abbsa = bool(pattern_abbsa.search(domain))
            has_abssa = bool(pattern_abssa.search(domain))
            has_absaa = bool(pattern_absaa.search(domain))

            if (has_coza or has_africa) and has_absa:
                golden_matches.append(domain)
            elif has_coza:
                coza_only.append(domain)
            elif has_absa:
                absa_only.append(domain)
            elif has_aabsa or has_abbsa or has_abssa or has_absaa:
                absa_typo_only.append(domain)
            elif has_africa:
                africa_only.append(domain)

    output_path = os.path.join(output_dir, filename)
    with open(output_path, "w", encoding="utf-8") as outfile:
        # Summary Header
        outfile.write(f"Summary for {filename}:\n")
        outfile.write(f"  - Golden Matches  : {len(golden_matches)}\n")
        outfile.write(f"  - .co.za Only     : {len(coza_only)}\n")
        outfile.write(f"  - absa Only       : {len(absa_only)}\n")
        outfile.write(f"  - absa Typos      : {len(absa_typo_only)}\n")
        outfile.write(f"  - .africa Only    : {len(africa_only)}\n")
        outfile.write("=" * 40 + "\n\n")

        # Detailed Sections
        outfile.write("=== Golden Matches ===\n")
        outfile.writelines(f"{d}\n" for d in golden_matches)

        outfile.write("\n=== .co.za Only Matches ===\n")
        outfile.writelines(f"{d}\n" for d in coza_only)

        outfile.write("\n=== absa Only Matches ===\n")
        outfile.writelines(f"{d}\n" for d in absa_only)

        outfile.write("\n=== absa Typo Matches ===\n")
        outfile.writelines(f"{d}\n" for d in absa_typo_only)


    print(f"[✓] {filename} → {output_path}")
    print(f"    - Golden Matches : {len(golden_matches)}")
    print(f"    - .co.za Only    : {len(coza_only)}")
    print(f"    - absa Only      : {len(absa_only)}")
    print(f"    - absa Typos     : {len(absa_typo_only)}")
    print(f"    - .africa Only   : {len(africa_only)}\n")

def main():
    if not os.path.exists(input_dir):
        print(f"[!] Input directory not found: {input_dir}")
        return

    for filename in sorted(os.listdir(input_dir)):
        file_path = os.path.join(input_dir, filename)
        if not os.path.isfile(file_path):
            continue
        parse_file(file_path, filename)

if __name__ == "__main__":
    main()
