# Enhanced Network Intrusion Detection Using Custom Suricata Rules

## Project Overview

This research project demonstrates an 800% improvement in network intrusion detection through the development and evaluation of 88 custom Suricata IDS rules.

## Key Results

- **Detection Rate**: 74.77% (vs 8.3% baseline)
- **Precision**: 93.82%
- **Recall**: 74.77%
- **F1 Score**: 83.22%
- **Improvement**: +800% over default configuration

## Repository Structure
```
project/
├── week1_setup/              # VM configuration
├── week2_services/           # Target services setup
├── week3_suricata/           # Suricata installation & rules
│   └── custom_rules/
│       ├── portscan.rules    # 17 port scan detection rules
│       ├── sqli.rules        # 28 SQL injection rules
│       ├── bruteforce.rules  # 26 brute force rules
│       └── exploits.rules    # 17 exploit detection rules
├── week4_experiments/        # 3 scenario testing
│   ├── scenario1_baseline/
│   ├── scenario2_enhanced/
│   └── scenario3_benign/
├── week5_analysis/           # Data analysis & visualization
│   ├── analyze_logs.py
│   ├── create_charts.py
│   └── charts/              # 5 professional visualizations
└── week6_paper/             # Documentation
    ├── ieee_paper_latex.tex
    ├── presentation_content.txt
    └── demo_script.md
```

## Quick Start

### Prerequisites
- VMware Workstation 17
- Ubuntu Server 22.04 / Desktop 22.04
- Kali Linux 2024.3
- Python 3.10+

### Installation
```bash
# 1. Setup VMs (Week 1-2)
# Follow setup guide in week1_setup/

# 2. Install Suricata from source
cd /home/student
git clone https://github.com/OISF/suricata.git
cd suricata
./autogen.sh
./configure --prefix=/usr --sysconfdir=/etc
make -j $(nproc)
sudo make install

# 3. Install custom rules
sudo cp custom_rules/*.rules /etc/suricata/rules/custom/
```

### Running Tests
```bash
# Scenario 1: Baseline
sudo systemctl stop suricata
# Edit config to disable custom rules
sudo systemctl start suricata
# Run attacks from Kali

# Scenario 2: Enhanced
# Edit config to enable custom rules
sudo systemctl restart suricata
# Run SAME attacks

# Scenario 3: Benign
# Run normal traffic
# Analyze false positives
```

### Analysis
```bash
cd week5_analysis
python3 -m venv venv
source venv/bin/activate
pip install pandas matplotlib seaborn
python3 analyze_logs.py
python3 create_charts.py
```

## Custom Rules

### Port Scanning (17 rules)
Detects TCP/UDP scans, ICMP sweeps, Nmap/Masscan signatures.

### SQL Injection (28 rules)
Covers UNION, Boolean, Time-based, Error-based SQLi patterns.

### Brute Force (26 rules)
Monitors SSH, FTP, HTTP, database authentication attempts.

### Exploits (17 rules)
Identifies RCE, command injection, LFI/RFI, XSS patterns.

## Results Summary

### Detection Comparison
| Scenario | Alerts | Detection Rate |
|----------|--------|----------------|
| Baseline | 54     | 8.3%          |
| Enhanced | 486    | 74.8%         |
| Improvement | +432 | +800%       |

### Category Breakdown (Enhanced)
| Category | Alerts | Percentage |
|----------|--------|-----------|
| Port Scans | 340  | 70.0%     |
| SQL Injection | 101 | 20.8%  |
| Brute Force | 30  | 6.2%      |

## Performance Metrics

- **Precision**: 0.9382 (93.82%)
- **Recall**: 0.7477 (74.77%)
- **F1 Score**: 0.8322 (83.22%)
- **False Positive Rate**: 160% (32 FP / 20 benign actions)

## Network Architecture
```
┌──────────────┐      ┌───────────────┐      ┌──────────────┐
│ Kali Linux   │◄────►│ br0 Bridge    │◄────►│ Target DVWA  │
│ 192.168...20 │      │               │      │ 192.168...30 │
│ Attacker     │      │      ▼        │      │ Vulnerable   │
└──────────────┘      │ Suricata IDS  │      └──────────────┘
                      │ 192.168...10  │
                      │ Monitor       │
                      └───────────────┘
```

## Citation

If you use this work, please cite:
```bibtex
@inproceedings{yourname2025enhanced,
  title={Enhanced Network Intrusion Detection Using Custom Suricata Rules: A Comparative Analysis},
  author={[Your Name]},
  booktitle={[Conference Name]},
  year={2025}
}
```

## License

This project is released under MIT License for educational purposes.

## Contact

- **Author**: [Your Name]
- **Email**: [your.email@university.edu]
- **University**: [University Name]

## Acknowledgments

- Suricata IDS team for the excellent open-source tool
- [Advisor Name] for guidance
- Computer Science Department for infrastructure support

---

**Last Updated**: December 17, 2025
**Project Status**: Complete ✅
**Documentation**: 100%
