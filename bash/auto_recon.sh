
#!/bin/bash

target=$1
timestamp=$(date +%Y-%m-%d_%H-%M-%S)
safe_target=$(echo "$target" | tr "." "_")
output="recon_${safe_target}_${timestamp}.txt"


if [ -z "$target" ]; then	
	echo "Usage: $0 pr <IP OR DOMAIN>"
	exit 1
fi

ports(){
        echo "[*] Running whatweb " | tee -a $output
        whatweb http://$target >> $output 2>/dev/null 
        echo -e "\n" >> $output

        echo "[*] Fetching HTTP Headers..." | tee -a $output
        curl -I http://$target >> $output 2>/dev/null
        echo -e "\n" >> $output

}

echo "[+] Starting recon on $target" 
echo "Recon Report for $target - $timestamp" > $output
echo "========================================" >> $output

echo "[1] Running Nmap Scan " | tee -a $output
nmap_output=$(nmap -T4 -F $target)
echo "$nmap_output" >> "$output" 
echo -e "\n" >> $output

if echo "$nmap_output" | grep -qE "80/tcp\s+open|443/tcp\s+open" ; then
	echo "[+] Port 80 or 443 is open" | tee -a $output
	ports
fi
echo "[2] Running whois " | tee -a $output
whois $target >> $output 2>/dev/null
echo -e "\n" >> $output

echo "[3] Running nslookup " | tee -a $output
nslookup $target >> $output
echo -e "\n" >> $output
