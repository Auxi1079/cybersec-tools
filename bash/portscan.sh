
read -p "Enter the IP you want to scan: " ip

echo "[->] Scanning $ip for open ports"
nmap -T4 $ip | grep "open" > ports_$ip.txt
echo "[->] Open ports saved to ports_$ip.txt"


