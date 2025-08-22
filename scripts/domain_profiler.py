import requests
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()
output_dir = os.path.join(os.path.dirname(__file__), "Output", "Domain_Profiles")
os.makedirs(output_dir, exist_ok=True)

# === API Keys ===
API_KEYS = {
    "viewdns": os.getenv("VIEW_DNS_API_KEY"),
    "virustotal": os.getenv("VIRUS_TOTAL_API_KEY"),
    "securitytrails": os.getenv("SECURITY_TRAILS_API_KEY")
}

# === ViewDNS Functions ===
def viewdns_propCheck(domain):
    """Fetch WHOIS info from ViewDNS."""
    print(f"[ViewDNS] WHOIS lookup for: {domain}")
    api_url = f'https://api.viewdns.info/propagation/?domain={domain}&apikey={API_KEYS["viewdns"]}&output=json'
    response = requests.get(api_url)

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return {}

    
def viewdns_reverse_ip(domain):
    """Fetch reverse IP info from ViewDNS."""
    api_url = f'https://api.viewdns.info/reversewhois/?q={domain}&apikey={API_KEYS["viewdns"]}&output=json'

    response = requests.get(api_url)

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return {}

def viewdns_whois(domain):
    """Fetch reverse IP info from ViewDNS."""
    api_url = f'https://api.viewdns.info/whois/v2/?domain={domain}&apikey={API_KEYS["viewdns"]}&output=json'

    response = requests.get(api_url)

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return {}

# === VirusTotal Functions ===
def virustotal_report(domain):
    """Fetch report from VirusTotal."""
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"

    headers = {
        "accept": "application/json",
        "x-apikey": API_KEYS["virustotal"]
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return {}
    

def virustotal_related_ips(domain):
    """Fetch related IPs or resolutions from VirusTotal."""
    api_url = f"https://www.virustotal.com/api/v3/domains/{domain}/related_ips"

    headers = {
        "accept": "application/json",
        "x-apikey": API_KEYS["virustotal"]
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return {}

# === SecurityTrails Functions ===
def securitytrails_subdomains(domain):
    """Fetch subdomains from SecurityTrails."""
    url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains?apikey={API_KEYS['securitytrails']}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return {}

def securitytrails_whois_history(domain):
    """Fetch WHOIS history from SecurityTrails."""
    url = f"https://api.securitytrails.com/v1/history/{domain}/whois?apikey={API_KEYS['securitytrails']}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return {}

def securitytrails_whois(domain):
    """Fetch WHOIS information from SecurityTrails."""
    url = f"https://api.securitytrails.com/v1/domain/{domain}/whois?apikey={API_KEYS['securitytrails']}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return {}


def securitytrails_domain(domain):
    """Fetch WHOIS information from SecurityTrails."""
    url = f"https://api.securitytrails.com/v1/domain/{domain}?apikey={API_KEYS['securitytrails']}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return {}
# === Domain Enrichment ===
def enrich_domain(domain):
    """Combine all data sources into a single profile."""
    result = {"domain": domain}

    # Create a JSON section for SecurityTrails
    result["securitytrails"] = {}
    # SecurityTrails
    result["securitytrails"].update(securitytrails_domain(domain))
    result["securitytrails"].update(securitytrails_subdomains(domain))


    #Create View DNS section
    result["viewdns"] = {}
    # ViewDNS
    result["viewdns"].update(viewdns_propCheck(domain))
    result["viewdns"].update(viewdns_whois(domain))

    # Create a JSON section for VirusTotal
    result["virustotal"] = {}
    # VirusTotal
    result["virustotal"].update(virustotal_report(domain))
    result["virustotal"].update(virustotal_related_ips(domain))



    # Save to file
    output_filename = f"{domain.replace('.', '_')}_profile.json"
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(result, outfile, indent=2, ensure_ascii=False)


    return result

# === Main Flow ===
def main(domain):
    report = enrich_domain(domain)
    print("\n[✓] Enriched Domain Report:")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main("nothingillegal.africa")
