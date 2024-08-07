import urllib.parse
import argparse
import threading
import re
import requests

def print_banner():
    print("""\033[1;32m
       ██████   █████   ██▓      ██████  ██▓▓█████▄ ▓█████ 
     ▒██    ▒ ▒██▓  ██▒▓██▒    ▒██    ▒ ▓██▒▒██▀ ██▌▓█   ▀ 
     ░ ▓██▄   ▒██▒  ██░▒██░    ░ ▓██▄   ▒██▒░██   █▌▒███   
       ▒   ██▒░██  █▀ ░▒██░      ▒   ██▒░██░░▓█▄   ▌▒▓█  ▄ 
     ▒██████▒▒░▒███▒█▄ ░██████▒▒██████▒▒░██░░▒████▓ ░▒████▒
     ▒ ▒▓▒ ▒ ░░░ ▒▒░ ▒ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░░▓   ▒▒▓  ▒ ░░ ▒░ ░
     ░ ░▒  ░ ░ ░ ▒░  ░ ░ ░ ▒  ░░ ░▒  ░ ░ ▒ ░ ░ ▒  ▒  ░ ░  ░
     ░  ░  ░     ░   ░   ░ ░   ░  ░  ░   ▒ ░ ░ ░  ░    ░   
           ░      ░        ░  ░      ░   ░     ░       ░  ░
                                         ░ by: wh0is\033[0;0m""")
    
def testing_sql(url, payload, proxies=None):
    try:
        encodb = urllib.parse.quote(payload)
        response = requests.get(url, params={'q': encodb})
        if re.search(re.escape(payload), response.text, re.IGNORECASE):
            print(f"\n  \033[1;32m[+] vulnerable! {url} with payload: {payload}\033[0;0m\n")
        else:
            print(f"\n  \033[1;31m[-] safe! {url} with payload: {payload}\033[0;0m\n")
    except requests.RequestException as error:
        print("[!] error: {}".format(error))

def scanning(payloadf, targetu, proxies):
    try:
        if not payloadf:
            print("  [!] no payload. bye...! :/")
            return
        
        with open(payloadf, 'r') as file:
            payloads = file.read().splitlines()
        
        for payload in payloads:
            testing_sql(targetu, payload)
        print("\n  bye...!\n")
    
    except Exception as e:
        print("  [!] error: {}".format(e))
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=print_banner())
    parser.add_argument('-p', '--payloads', type=str, required=True, help='path to the payloads file')
    parser.add_argument('-t', '--target', type=str, required=True, help='target url')
    parser.add_argument('--proxy', type=str, help='proxy server in the format http://user:pass@host:port')
    args = parser.parse_args()
    

    proxies = None
    if args.proxy:

        proxies = {

	    'http': args.proxy,
	    'https': args.proxy,

	}

    try:
       threading.Thread(target=scanning, args=(args.payloads, args.target, proxies)).start()
    except KeyboardInterrupt:
        print("\n\n    ...bye...!\n")
        exit()
    
