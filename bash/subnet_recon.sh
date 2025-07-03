#!/bin/bash

base=$1
timestamp=$(date +%Y-%m-%d_%H-%M-%S)
safe_base=$(echo "$base" | tr "." "_")
output="subnet_recon_${safe_base}_${timestamp}.txt"

if [ -z "$base" ]; then
    echo "Usage: $0 <Base IP> (e.g. 192.168.1)"
    exit 1
fi

echo "🔎 Starting full subnet recon on $base.0/24" | tee -a $output

for i in {1..254}; do
    ip="$base.$i"
    echo "Pinging $ip..." | tee -a $output
    ping -c 1 -W 1 $ip > /dev/null

    if [ $? -eq 0 ]; then
        echo "[+] Host $ip is UP" | tee -a $output
        echo "[*] Scanning $ip with nmap..." | tee -a $output
        nmap -T4 -F $ip >> $output

        open_ports=$(nmap -T4 -F $ip | grep "open" | cut -d "/" -f1)

        if echo "$open_ports" | grep -qE "80|443"; then
            echo "[*] Running curl and whatweb on $ip..." | tee -a $output
            curl -I http://$ip --max-time 3 >> $output 2>/dev/null
            whatweb http://$ip >> $output 2>/dev/null
        fi

        echo -e "-----------------------------------\n" >> $output
    else
        echo "[-] Host $ip is DOWN" >> $output
    fi
done

echo "✅ Subnet recon completed. Report saved to $output"

