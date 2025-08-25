import requests
import os
from dotenv import load_dotenv

load_dotenv()
q = 'absa.work'
apikey = os.getenv("VIEW_DNS_API_KEY")
output = 'json'
if apikey is None:
    raise ValueError("VIEW_DNS_API_KEY not set in environment variables.")

api_url = f'https://api.viewdns.info/subdomains/?domain={q}&apikey={apikey}&output={output}'

response = requests.get(api_url)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")