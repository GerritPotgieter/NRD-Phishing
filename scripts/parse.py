import os
import re

# Define paths
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
input_file = os.path.join(root_dir, "NRDs", "nrd-14day.txt")
output_file = os.path.join(root_dir, "Output", "matched_domains2.txt")

# Define regex patterns
pattern_coza = re.compile(r"\.co\.za$", re.IGNORECASE)
pattern_absa = re.compile(r"absa", re.IGNORECASE)

def main():
    if not os.path.exists(input_file):
        print(f"[!] Input file not found: {input_file}")
        return

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Categorized match lists
    coza_only = []
    absa_only = []
    golden_matches = []

    with open(input_file, "r", encoding="utf-8", errors="ignore") as infile:
        for line in infile:
            domain = line.strip()
            if not domain:
                continue

            has_coza = bool(pattern_coza.search(domain))
            has_absa = bool(pattern_absa.search(domain))

            if has_coza and has_absa:
                golden_matches.append(domain)
            elif has_coza:
                coza_only.append(domain)
            elif has_absa:
                absa_only.append(domain)

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("=== Golden Matches (absa + .co.za) ===\n")
        for match in golden_matches:
            outfile.write(match + "\n")

        outfile.write("\n=== .co.za Only Matches ===\n")
        for match in coza_only:
            outfile.write(match + "\n")

        outfile.write("\n=== absa Only Matches ===\n")
        for match in absa_only:
            outfile.write(match + "\n")

    print(f"[✓] Done! Output written to {output_file}")
    print(f"    - Golden Matches : {len(golden_matches)}")
    print(f"    - .co.za Only    : {len(coza_only)}")
    print(f"    - absa Only      : {len(absa_only)}")

if __name__ == "__main__":
    main()
