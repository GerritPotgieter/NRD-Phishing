import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from parse import parse_file as parse_nrd_file
from parse_full import parse_file as parse_full_file
from domain_profiler import enrich_domain

class NRDPhishingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NRD Phishing Toolkit")
        self.geometry("900x600")

        self.tab_control = ttk.Notebook(self)

        self.download_tab = ttk.Frame(self.tab_control)
        self.enrich_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.download_tab, text="📥 Download & Parse")
        self.tab_control.add(self.enrich_tab, text="🔍 Enrich Domain")
        self.tab_control.pack(expand=1, fill="both")

        self.setup_download_tab()
        self.setup_enrich_tab()

    def setup_download_tab(self):
        # Download Button
        self.download_button = ttk.Button(self.download_tab, text="Download NRD Lists", command=self.fake_download)
        self.download_button.pack(pady=10)

        # Parse Button
        self.parse_button = ttk.Button(self.download_tab, text="Parse Lists", command=self.parse)
        self.parse_button.pack(pady=10)

        # Output Area
        self.output_area = scrolledtext.ScrolledText(self.download_tab, wrap=tk.WORD, width=100, height=25)
        self.output_area.pack(padx=10, pady=10)

    def setup_enrich_tab(self):
        self.domain_label = ttk.Label(self.enrich_tab, text="Enter Domain:")
        self.domain_label.pack(pady=(10, 0))

        self.domain_entry = ttk.Entry(self.enrich_tab, width=50)
        self.domain_entry.pack(pady=5)

        self.enrich_button = ttk.Button(self.enrich_tab, text="Enrich", command=self.fake_enrich)
        self.enrich_button.pack(pady=10)

        self.enrich_output = scrolledtext.ScrolledText(self.enrich_tab, wrap=tk.WORD, width=100, height=25)
        self.enrich_output.pack(padx=10, pady=10)





    def fake_download(self):
        # Simulate file download
        files_downloaded = ["2025-08-01", "2025-08-02", "2025-08-03"]
        messagebox.showinfo("Download Complete", f"Fetched {len(files_downloaded)} lists.")
        self.output_area.insert(tk.END, f"Downloaded Files: {', '.join(files_downloaded)}\n")

    def parse(self):
        # Simulate parsing
        try:
            parse_nrd_file("nrd-60days-free.txt", "parsed_output.txt")
            parse_full_file("nrd-60days-free.txt", "full_parsed_output.txt")
            messagebox.showinfo("Parse Complete", "Files parsed successfully.")
            self.output_area.insert(tk.END, "Parsed files: parsed_output.txt, full_parsed_output.txt\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse files: {e}")



    def fake_enrich(self):
        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showwarning("Input Required", "Please enter a domain name.")
            return

        enrich_domain(domain)
        self.enrich_output.delete(1.0, tk.END)
        self.enrich_output.insert(tk.END, json.dumps(enrich_domain(domain), indent=4))
        messagebox.showinfo("Enrichment Complete", f"Domain {domain} enriched successfully.")


if __name__ == "__main__":
    app = NRDPhishingApp()
    app.mainloop()
