import os
import shodan
from dotenv import load_dotenv

load_dotenv()

SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
IP_ADDRESS = "13.247.33.149"

if SHODAN_API_KEY is None:
    raise ValueError("SHODAN_API_KEY not set in environment variables.")

api = shodan.Shodan(SHODAN_API_KEY)

try:
    host = api.host(IP_ADDRESS)

    print(f"[+] Host: {host['ip_str']}")
    print(f"[+] Organization: {host.get('org', 'n/a')}")
    print(f"[+] ISP: {host.get('isp', 'n/a')}")
    print(f"[+] OS: {host.get('os', 'n/a')}")
    print(f"[+] Last Update: {host.get('last_update', 'n/a')}")
    print(f"[+] Hostnames: {host.get('hostnames', [])}")
    print(f"[+] Open Ports: {host.get('ports', [])}")
    print("\n[+] Services:")
    for item in host['data']:
        print(f" - Port: {item['port']}")
        print(f"   Product: {item.get('product', 'n/a')}")
        print(f"   Banner: {item['data'][:100]}...\n")  # Only show first 100 chars

except shodan.APIError as e:
    print(f"[!] Shodan API error: {e}")
except Exception as e:
    print(f"[!] General error: {e}")
