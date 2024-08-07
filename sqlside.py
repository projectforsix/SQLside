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

def testing_sql(url, payload, proxy=None):
    try:
        encodb = urllib.parse.quote(payload)
        proxies = {
            'http': proxy,
            'https': proxy
        } if proxy else None
        response = requests.get(url, params={'q': encodb}, proxies=proxies)
        if re.search(re.escape(payload), response.text, re.IGNORECASE):
            print(f"\n  \033[1;32m[+] vulnerable! {url} with payload: {payload}\033[0;0m\n")
        else:
            print(f"\n  \033[1;31m[-] safe! {url} with payload: {payload}\033[0;0m\n")
    except requests.RequestException as error:
        print("[!] error: {}".format(error))

def scanning(payloadf, targetu, proxy):
    try:
        if not payloadf:
            print("  [!] no payload. bye...! :/")
            return

        with open(payloadf, 'r') as file:
            payloads = file.read().splitlines()

        for payload in payloads:
            testing_sql(targetu, payload, proxy)
        print("\n  bye...!\n")

    except Exception as e:
        print("  [!] error: {}".format(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=print_banner())
    parser.add_argument('-p', '--payloads', type=str, required=True, help='path to the payloads file')
    parser.add_argument('-t', '--target', type=str, required=True, help='target url')
    parser.add_argument('--proxy', type=str, help='proxy to use, e.g., http://127.0.0.1:8080')

    args = parser.parse_args()

    try:
        threading.Thread(target=scanning, args=(args.payloads, args.target, args.proxy)).start()
    except KeyboardInterrupt:
        print("\n\n    ...bye...!\n")
        exit()
