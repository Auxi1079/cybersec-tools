import argparse
import socket
import threading
import datetime
from scapy.all import IP, TCP, sr1

# -------------------------------
# Argument parsing
# -------------------------------
parser = argparse.ArgumentParser(description="Python Port Scanner with Stealth or Connect Scan")
parser.add_argument("target", help="IP or domain to scan")
parser.add_argument("-p", "--ports", help="Port range (e.g., 1-1000)", default="1-100")
parser.add_argument("--stealth", action="store_true", help="Use stealth SYN scan instead of full connect scan")

args = parser.parse_args()

start_port, end_port = map(int, args.ports.split("-"))
target = args.target
open_ports = []

# -------------------------------
# Stealth SYN scan
# -------------------------------
def stealth_syn_scan(ip, port):
    pkt = IP(dst=ip)/TCP(dport=port, flags="S")
    resp = sr1(pkt, timeout=1, verbose=0)

    if resp is None:
        return False
    elif resp.haslayer(TCP) and resp[TCP].flags == 0x12:
        rst = IP(dst=ip)/TCP(dport=port, flags="R")
        sr1(rst, timeout=1, verbose=0)
        return True
    else:
        return False

# -------------------------------
# Banner grabber
# -------------------------------
def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        banner = s.recv(1024).decode().strip()
        s.close()
        return banner
    except:
        return ""

# -------------------------------
# Port scanner (decides mode)
# -------------------------------
def scan_port(ip, port):
    try:
        if args.stealth:
            if stealth_syn_scan(ip, port):
                print(f"[+] Port {port} is OPEN (stealth)")
                log_open_port(ip, port)
        else:
            s = socket.socket()
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            if result == 0:
                print(f"[+] Port {port} is OPEN")
                banner = grab_banner(ip, port)
                log_open_port(ip, port, banner)
            s.close()
    except:
        pass

# -------------------------------
# Logger
# -------------------------------
def log_open_port(ip, port, banner=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {ip}:{port} open - {banner if banner else 'No banner'}"
    open_ports.append(line)

# -------------------------------
# Multithreaded scanning
# -------------------------------
threads = []
for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan_port, args=(target, port))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# -------------------------------
# Save output to log file
# -------------------------------
timestamp_for_file = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"scanlog_{target.replace('.', '_')}_{timestamp_for_file}.txt"

with open(log_filename, "w") as f:
    f.write(f"Scan results for {target} at {timestamp_for_file}:\n")
    f.write("=" * 50 + "\n")
    for entry in open_ports:
        f.write(entry + "\n")

print(f"[+] Scan complete. Results saved to {log_filename}")
