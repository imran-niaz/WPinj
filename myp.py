import requests
from bs4 import BeautifulSoup

# Function to check if a website is using WordPress
def check_wordpress(url):
    try:
        r = requests.get(url + "/wp-login.php")
        if r.status_code == 200:
            return True
    except:
        return False

# Function to enumerate WordPress plugins
def enumerate_plugins(url):
    try:
        r = requests.get(url + "/wp-content/plugins/")
        soup = BeautifulSoup(r.content, 'html.parser')
        plugins = [a.get('href') for a in soup.find_all('a', href=True)]
        return plugins
    except:
        return []

# Function to check if a plugin is vulnerable
def check_vulnerability(url, plugin):
    try:
        r = requests.get("https://wpvulndb.com/vulnerabilities/" + plugin)
        soup = BeautifulSoup(r.content, 'html.parser')
        if "No vulnerabilities found" in soup.get_text():
            return False
        else:
            return True
    except:
        return None

# Example usage
url = "https://example.com"
if check_wordpress(url):
    print("[+] Website is using WordPress.")
    plugins = enumerate_plugins(url)
    if plugins:
        print("[+] Enumerated plugins:")
        for plugin in plugins:
            if check_vulnerability(url, plugin):
                print("[+] " + plugin + " is vulnerable.")
            else:
                print("[-] " + plugin + " is not vulnerable.")
    else:
        print("[-] Failed to enumerate plugins.")
else:
    print("[-] Website is not using WordPress.")
