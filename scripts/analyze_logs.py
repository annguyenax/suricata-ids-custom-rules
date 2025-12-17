#!/usr/bin/env python3
"""
Suricata IDS Log Analysis Script
Analyzes 3 scenarios and generates metrics
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from datetime import datetime

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

class SuricataAnalyzer:
    def __init__(self, base_dir='/home/student/experiment_results'):
        self.base_dir = base_dir
        self.scenarios = {
            'baseline': f'{base_dir}/scenario1_baseline_real',
            'enhanced': f'{base_dir}/scenario2_enhanced_real',
            'benign': f'{base_dir}/scenario3_benign_real'
        }
        
    def parse_fast_log(self, log_file):
        """Parse fast.log file"""
        alerts = []
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if '[**]' in line:
                        parts = line.strip().split('[**]')
                        if len(parts) >= 3:
                            timestamp = parts[0].strip()
                            sig_info = parts[1].strip()
                            classification = parts[2].strip() if len(parts) > 2 else ''
                            
                            # Extract SID
                            sid = None
                            if '[1:' in sig_info:
                                sid_part = sig_info.split('[1:')[1].split(']')[0]
                                sid = f"1:{sid_part}"
                            
                            alerts.append({
                                'timestamp': timestamp,
                                'signature': sig_info,
                                'classification': classification,
                                'sid': sid,
                                'raw': line.strip()
                            })
        except Exception as e:
            print(f"Error parsing {log_file}: {e}")
        
        return pd.DataFrame(alerts)
    
    def analyze_scenario(self, scenario_name):
        """Analyze a single scenario"""
        log_path = f"{self.scenarios[scenario_name]}/fast.log"
        print(f"\n{'='*60}")
        print(f"Analyzing {scenario_name.upper()} Scenario")
        print(f"{'='*60}")
        
        df = self.parse_fast_log(log_path)
        
        if df.empty:
            print(f"No alerts found in {log_path}")
            return None
        
        # Basic statistics
        total_alerts = len(df)
        unique_sids = df['sid'].nunique()
        
        print(f"Total Alerts: {total_alerts}")
        print(f"Unique Rules Triggered: {unique_sids}")
        
        # Count by category
        categories = {
            'PORTSCAN': df['signature'].str.contains('PORTSCAN', case=False, na=False).sum(),
            'SQLI': df['signature'].str.contains('SQLI|SQL', case=False, na=False).sum(),
            'BRUTEFORCE': df['signature'].str.contains('BRUTEFORCE|Brute', case=False, na=False).sum(),
            'Other': 0
        }
        categories['Other'] = total_alerts - sum([v for k, v in categories.items() if k != 'Other'])
        
        print(f"\nBreakdown by Category:")
        for cat, count in categories.items():
            print(f"  {cat}: {count}")
        
        # Top 10 rules
        print(f"\nTop 10 Most Triggered Rules:")
        top_rules = df['sid'].value_counts().head(10)
        for sid, count in top_rules.items():
            print(f"  {sid}: {count} alerts")
        
        return {
            'name': scenario_name,
            'total_alerts': total_alerts,
            'unique_sids': unique_sids,
            'categories': categories,
            'top_rules': top_rules,
            'dataframe': df
        }
    
    def compare_scenarios(self):
        """Compare all scenarios"""
        results = {}
        
        for scenario in ['baseline', 'enhanced', 'benign']:
            results[scenario] = self.analyze_scenario(scenario)
        
        return results
    
    def calculate_metrics(self, results):
        """Calculate detection metrics"""
        print(f"\n{'='*60}")
        print("DETECTION METRICS CALCULATION")
        print(f"{'='*60}")
        
        baseline = results['baseline']['total_alerts']
        enhanced = results['enhanced']['total_alerts']
        false_pos = results['benign']['total_alerts']
        
        # Attack profile (known from testing)
        total_attacks = 650  # 500 port scans + 100 SQLi + 50 SSH
        
        # Calculate metrics for enhanced scenario
        true_positives = enhanced  # Alerts on malicious traffic
        false_positives = false_pos  # Alerts on benign traffic
        false_negatives = total_attacks - enhanced  # Attacks missed
        
        # Metrics
        detection_rate = (enhanced / total_attacks) * 100
        false_positive_rate = (false_positives / 20) * 100  # 20 benign actions
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        improvement = ((enhanced - baseline) / baseline * 100) if baseline > 0 else 0
        
        metrics = {
            'Detection Rate': f"{detection_rate:.2f}%",
            'False Positive Rate': f"{false_positive_rate:.2f}%",
            'Precision': f"{precision:.4f}",
            'Recall': f"{recall:.4f}",
            'F1 Score': f"{f1_score:.4f}",
            'Improvement over Baseline': f"+{improvement:.0f}%"
        }
        
        print("\nEnhanced Scenario Metrics:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value}")
        
        return metrics

def main():
    print("="*60)
    print("SURICATA IDS - LOG ANALYSIS")
    print("="*60)
    
    analyzer = SuricataAnalyzer()
    results = analyzer.compare_scenarios()
    metrics = analyzer.calculate_metrics(results)
    
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETED ✓")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
