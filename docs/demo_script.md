# DEMONSTRATION SCRIPT
## Suricata IDS Custom Rules Demo

### DEMO OVERVIEW
**Duration:** 10-15 minutes
**Objective:** Show live detection of attacks using custom rules

---

### PART 1: ENVIRONMENT OVERVIEW (2 min)

**Script:**
"Let me show you our experimental environment. We have three virtual machines:
- Suricata IDS at 192.168.100.10 - our intrusion detection system
- Target system at 192.168.100.30 - running DVWA vulnerable web application
- Kali Linux at 192.168.100.20 - our attack platform

The network traffic flows through a bridge interface that Suricata monitors."

**Show:**
```bash
# On Suricata-IDS
ip addr show br0
sudo systemctl status suricata | head -10
```

---

### PART 2: CUSTOM RULES DEMONSTRATION (3 min)

**Script:**
"We developed 88 custom rules. Let me show you a few examples:"

**Show:**
```bash
# Port scan rule
sudo head -5 /etc/suricata/rules/custom/portscan.rules

# SQL injection rule
sudo grep "1000111" /etc/suricata/rules/custom/sqli.rules

# SSH brute force rule
sudo grep "1000301" /etc/suricata/rules/custom/bruteforce.rules
```

**Explain threshold-based detection**

---

### PART 3: LIVE ATTACK DETECTION (5 min)

**Script:**
"Now I'll demonstrate live detection. First, let's clear the logs and monitor in real-time."

**Prepare:**
```bash
# On Suricata-IDS
sudo truncate -s 0 /var/log/suricata/fast.log

# Start tailing logs
sudo tail -f /var/log/suricata/fast.log
```

**Execute Attacks from Kali:**
```bash
# Port scan
echo "Executing port scan..."
nmap -Pn -sS 192.168.100.30 -p 20-100

# SQL injection
echo "Executing SQL injection..."
curl "http://192.168.100.30/login.php?user=admin%27%20OR%201=1"

# SSH brute force
echo "Executing SSH brute force..."
for i in {1..10}; do
    timeout 1 ssh fake$i@192.168.100.30 2>/dev/null
done
```

**Point out alerts appearing in tail window**

---

### PART 4: ANALYSIS VISUALIZATION (3 min)

**Script:**
"Here are our analysis results comparing baseline and enhanced configurations."

**Show Charts:**
```bash
# Open charts
cd /home/student/week5_analysis
xdg-open chart_1_comparison.png
xdg-open chart_2_categories.png
xdg-open chart_5_metrics_table.png
```

**Highlight:**
- 800% improvement
- Category distribution
- Performance metrics

---

### PART 5: CONCLUSION (2 min)

**Script:**
"In summary, our custom rules achieved:
- 800% improvement in detection
- 93% precision
- 75% recall
- Only 32 false positives in benign traffic

This demonstrates that tailored rules significantly enhance detection while maintaining operational efficiency."

**Final Show:**
```bash
# Show final statistics
cat /home/student/experiment_results/REAL_COMPARISON_REPORT.txt | head -50
```

---

### BACKUP: TROUBLESHOOTING

**If Suricata not running:**
```bash
sudo systemctl start suricata
sleep 10
sudo systemctl status suricata
```

**If no alerts appearing:**
```bash
# Check Suricata is processing
sudo grep "decoder.pkts" /var/log/suricata/stats.log | tail -1

# Verify custom rules loaded
sudo grep "rules loaded" /var/log/suricata/suricata.log | tail -1
```

**If network issues:**
```bash
# Verify connectivity
ping -c 3 192.168.100.30

# Check br0 status
ip link show br0
```

---

**END OF DEMO SCRIPT**
