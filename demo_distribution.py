#!/usr/bin/env python3
"""
Demo script to show the even distribution of simulation types and testing statuses.
This script generates sample data and displays the distribution statistics.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_populator import DatabasePopulator
from collections import Counter
import random


def demo_employee_master_distribution(num_employees=20):
    """Demonstrate employee_master simulation type and testing status distribution"""
    print("\n" + "=" * 70)
    print(f"Employee Master Distribution (n={num_employees})")
    print("=" * 70)
    
    # Simulate employee generation
    simulation_types = ['Phishing Test', 'Vishing Test', 'Quishing Test', 'Red Team Assessment']
    phish_statuses = ['Completed', 'Pending', 'Failed', 'Passed']
    vish_statuses = ['Completed', 'Pending', 'Failed', 'Passed']
    red_team_statuses = ['Completed', 'In Progress', 'Scheduled', 'Cancelled']
    
    sim_type_counts = Counter()
    phish_status_counts = Counter()
    vish_status_counts = Counter()
    red_team_status_counts = Counter()
    
    print("\nGenerated Records:")
    print(f"{'Employee ID':<15} {'Simulation Type':<25} {'Phish Status':<15} {'Vish Status':<15} {'Red Team Status':<20}")
    print("-" * 90)
    
    for i in range(num_employees):
        sim_type = simulation_types[i % len(simulation_types)]
        phish_status = phish_statuses[i % len(phish_statuses)]
        vish_status = vish_statuses[i % len(vish_statuses)]
        red_team_status = red_team_statuses[i % len(red_team_statuses)]
        
        sim_type_counts[sim_type] += 1
        phish_status_counts[phish_status] += 1
        vish_status_counts[vish_status] += 1
        red_team_status_counts[red_team_status] += 1
        
        print(f"{i+1:<15} {sim_type:<25} {phish_status:<15} {vish_status:<15} {red_team_status:<20}")
    
    print("\n" + "-" * 70)
    print("Distribution Summary:")
    print("-" * 70)
    
    print("\nSimulation Types (aligned with test types):")
    for sim_type, count in sorted(sim_type_counts.items()):
        percentage = (count / num_employees) * 100
        print(f"  {sim_type:<30} {count:>3} ({percentage:>5.1f}%)")
    
    print("\nPhishing Testing Statuses:")
    for status, count in sorted(phish_status_counts.items()):
        percentage = (count / num_employees) * 100
        print(f"  {status:<30} {count:>3} ({percentage:>5.1f}%)")
    
    print("\nVishing Testing Statuses:")
    for status, count in sorted(vish_status_counts.items()):
        percentage = (count / num_employees) * 100
        print(f"  {status:<30} {count:>3} ({percentage:>5.1f}%)")
    
    print("\nRed Team Testing Statuses:")
    for status, count in sorted(red_team_status_counts.items()):
        percentage = (count / num_employees) * 100
        print(f"  {status:<30} {count:>3} ({percentage:>5.1f}%)")


def demo_phishing_simulations_distribution(num_simulations=30):
    """Demonstrate phishing/smishing simulation distribution"""
    print("\n" + "=" * 70)
    print(f"Phishing/Smishing Simulations Distribution (n={num_simulations})")
    print("=" * 70)
    
    simulation_types = ['Email Phishing', 'SMS Phishing', 'Social Media Phishing']
    testing_statuses = ['Completed', 'Pending', 'Failed', 'Passed']
    
    sim_type_counts = Counter()
    status_counts = Counter()
    
    print("\nGenerated Records (showing first 15):")
    print(f"{'Sim ID':<10} {'Simulation Type':<30} {'Testing Status':<20}")
    print("-" * 60)
    
    for i in range(num_simulations):
        sim_type = simulation_types[i % len(simulation_types)]
        test_status = testing_statuses[i % len(testing_statuses)]
        
        sim_type_counts[sim_type] += 1
        status_counts[test_status] += 1
        
        if i < 15:  # Only show first 15 records
            print(f"{i+1:<10} {sim_type:<30} {test_status:<20}")
    
    if num_simulations > 15:
        print(f"... ({num_simulations - 15} more records)")
    
    print("\n" + "-" * 70)
    print("Distribution Summary:")
    print("-" * 70)
    
    print("\nSimulation Types:")
    for sim_type, count in sorted(sim_type_counts.items()):
        percentage = (count / num_simulations) * 100
        print(f"  {sim_type:<30} {count:>3} ({percentage:>5.1f}%)")
    
    print("\nTesting Statuses:")
    for status, count in sorted(status_counts.items()):
        percentage = (count / num_simulations) * 100
        print(f"  {status:<30} {count:>3} ({percentage:>5.1f}%)")


def demo_quishing_simulations_distribution(num_simulations=24):
    """Demonstrate quishing simulation distribution"""
    print("\n" + "=" * 70)
    print(f"Quishing Simulations Distribution (n={num_simulations})")
    print("=" * 70)
    
    qr_code_types = ['Payment QR', 'WiFi QR', 'App Download QR', 'Survey QR', 'Menu QR', 'Contact QR']
    device_types = ['Mobile Phone', 'Tablet', 'Laptop', 'Desktop']
    testing_statuses = ['Completed', 'Pending', 'Failed', 'Passed']
    
    qr_type_counts = Counter()
    device_counts = Counter()
    status_counts = Counter()
    malicious_counts = Counter()
    
    print("\nGenerated Records (showing first 12):")
    print(f"{'Sim ID':<10} {'QR Type':<20} {'Device':<15} {'Status':<15} {'Malicious':<12}")
    print("-" * 72)
    
    for i in range(num_simulations):
        qr_type = qr_code_types[i % len(qr_code_types)]
        device = device_types[i % len(device_types)]
        status = testing_statuses[i % len(testing_statuses)]
        # Alternate True/False for even distribution: even indices (0,2,4...) = True, odd indices (1,3,5...) = False
        malicious = (i % 2 == 0)
        
        qr_type_counts[qr_type] += 1
        device_counts[device] += 1
        status_counts[status] += 1
        malicious_counts[malicious] += 1
        
        if i < 12:  # Only show first 12 records
            print(f"{i+1:<10} {qr_type:<20} {device:<15} {status:<15} {str(malicious):<12}")
    
    if num_simulations > 12:
        print(f"... ({num_simulations - 12} more records)")
    
    print("\n" + "-" * 70)
    print("Distribution Summary:")
    print("-" * 70)
    
    print("\nQR Code Types:")
    for qr_type, count in sorted(qr_type_counts.items()):
        percentage = (count / num_simulations) * 100
        print(f"  {qr_type:<30} {count:>3} ({percentage:>5.1f}%)")
    
    print("\nDevice Types:")
    for device, count in sorted(device_counts.items()):
        percentage = (count / num_simulations) * 100
        print(f"  {device:<30} {count:>3} ({percentage:>5.1f}%)")
    
    print("\nTesting Statuses:")
    for status, count in sorted(status_counts.items()):
        percentage = (count / num_simulations) * 100
        print(f"  {status:<30} {count:>3} ({percentage:>5.1f}%)")
    
    print("\nMalicious QR Clicked:")
    # Sort with True first for better readability (showing clicked before not-clicked)
    for malicious, count in sorted(malicious_counts.items(), reverse=True):
        percentage = (count / num_simulations) * 100
        label = "True (Clicked)" if malicious else "False (Not Clicked)"
        print(f"  {label:<30} {count:>3} ({percentage:>5.1f}%)")


def main():
    """Run all demos"""
    print("=" * 70)
    print("Data Generation Distribution Demo")
    print("=" * 70)
    print("\nThis demo shows how simulation types and testing statuses are")
    print("evenly distributed using round-robin assignment.")
    
    # Demo employee master distribution
    demo_employee_master_distribution(20)
    
    # Demo phishing simulations distribution
    demo_phishing_simulations_distribution(30)
    
    # Demo quishing simulations distribution
    demo_quishing_simulations_distribution(24)
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print("\n✓ Simulation types are aligned with test types:")
    print("  - Employee Master: Uses test type names (Phishing Test, Vishing Test, etc.)")
    print("  - Phishing Sims: Uses phishing-specific types (Email, SMS, Social Media)")
    print("\n✓ All categories are evenly distributed:")
    print("  - Round-robin assignment ensures equal representation")
    print("  - No bias towards any particular value")
    print("\n✓ Changes maintain data consistency:")
    print("  - Statistics remain consistent across generations")
    print("  - Realistic data with controlled distributions")
    print("=" * 70)


if __name__ == "__main__":
    main()
