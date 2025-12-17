#!/usr/bin/env python3
"""
Create visualizations for Suricata analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def create_comparison_chart():
    """Bar chart comparing 3 scenarios"""
    scenarios = ['Baseline', 'Enhanced', 'Benign']
    alerts = [54, 486, 32]
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(scenarios, alerts, color=colors, alpha=0.8)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.title('Alert Comparison Across 3 Scenarios', fontsize=16, fontweight='bold')
    plt.ylabel('Number of Alerts', fontsize=12)
    plt.xlabel('Scenario', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/student/week5_analysis/chart_1_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Created: chart_1_comparison.png")
    plt.close()

def create_category_breakdown():
    """Pie chart showing category breakdown for Enhanced scenario"""
    categories = ['Port Scan', 'SQL Injection', 'Brute Force', 'Other']
    values = [340, 101, 30, 15]
    colors = ['#3498db', '#e74c3c', '#f39c12', '#95a5a6']
    explode = (0.1, 0, 0, 0)  # Explode port scan slice
    
    plt.figure(figsize=(10, 8))
    plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=90,
            colors=colors, explode=explode, shadow=True)
    plt.title('Enhanced Scenario - Alert Distribution by Category', 
              fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/student/week5_analysis/chart_2_categories.png', dpi=300, bbox_inches='tight')
    print("✓ Created: chart_2_categories.png")
    plt.close()

def create_improvement_chart():
    """Bar chart showing improvement"""
    categories = ['Port Scans', 'SQL Injection', 'SSH Brute Force']
    baseline = [20, 5, 10]
    enhanced = [340, 101, 30]
    
    x = np.arange(len(categories))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars1 = ax.bar(x - width/2, baseline, width, label='Baseline', color='#e74c3c', alpha=0.8)
    bars2 = ax.bar(x + width/2, enhanced, width, label='Enhanced', color='#2ecc71', alpha=0.8)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10)
    
    ax.set_xlabel('Attack Type', fontsize=12)
    ax.set_ylabel('Number of Alerts', fontsize=12)
    ax.set_title('Detection Improvement: Baseline vs Enhanced', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/student/week5_analysis/chart_3_improvement.png', dpi=300, bbox_inches='tight')
    print("✓ Created: chart_3_improvement.png")
    plt.close()

def create_detection_rate_chart():
    """Line chart showing detection rates"""
    scenarios = ['Baseline\n(Default)', 'Enhanced\n(+Custom)', 'Improvement']
    rates = [8.3, 74.8, 800]
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = '#2ecc71'
    ax1.set_xlabel('Scenario', fontsize=12)
    ax1.set_ylabel('Detection Rate (%)', color=color, fontsize=12)
    ax1.plot(scenarios[:2], rates[:2], marker='o', markersize=10, 
             linewidth=3, color=color, label='Detection Rate')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    # Add value labels
    for i, (x, y) in enumerate(zip(scenarios[:2], rates[:2])):
        ax1.text(i, y + 5, f'{y}%', ha='center', fontsize=12, fontweight='bold')
    
    ax2 = ax1.twinx()
    color = '#3498db'
    ax2.set_ylabel('Improvement (%)', color=color, fontsize=12)
    ax2.bar(scenarios[2], rates[2], color=color, alpha=0.5, label='Improvement')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.text(2, rates[2] + 50, f'+{rates[2]}%', ha='center', fontsize=12, fontweight='bold')
    
    plt.title('Detection Rate & Improvement Analysis', fontsize=16, fontweight='bold')
    fig.tight_layout()
    plt.savefig('/home/student/week5_analysis/chart_4_detection_rate.png', dpi=300, bbox_inches='tight')
    print("✓ Created: chart_4_detection_rate.png")
    plt.close()

def create_metrics_table():
    """Create metrics comparison table as image"""
    metrics_data = {
        'Metric': ['Total Alerts', 'Detection Rate', 'False Positives', 
                   'Precision', 'Recall', 'F1 Score'],
        'Baseline': ['54', '8.3%', 'N/A', '0.63', '0.08', '0.15'],
        'Enhanced': ['486', '74.8%', '32', '0.94', '0.75', '0.83']
    }
    
    df = pd.DataFrame(metrics_data)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(cellText=df.values, colLabels=df.columns,
                     cellLoc='center', loc='center',
                     colColours=['#3498db']*3)
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2)
    
    # Style header
    for i in range(len(df.columns)):
        table[(0, i)].set_facecolor('#3498db')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, len(df) + 1):
        for j in range(len(df.columns)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#ecf0f1')
    
    plt.title('Performance Metrics Comparison', fontsize=16, fontweight='bold', pad=20)
    plt.savefig('/home/student/week5_analysis/chart_5_metrics_table.png', dpi=300, bbox_inches='tight')
    print("✓ Created: chart_5_metrics_table.png")
    plt.close()

def main():
    print("\n" + "="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60 + "\n")
    
    create_comparison_chart()
    create_category_breakdown()
    create_improvement_chart()
    create_detection_rate_chart()
    create_metrics_table()
    
    print("\n" + "="*60)
    print("ALL CHARTS CREATED ✓")
    print("="*60)
    print("\nCharts saved in: /home/student/week5_analysis/")
    print("\nFiles created:")
    print("  1. chart_1_comparison.png")
    print("  2. chart_2_categories.png")
    print("  3. chart_3_improvement.png")
    print("  4. chart_4_detection_rate.png")
    print("  5. chart_5_metrics_table.png")

if __name__ == "__main__":
    main()
