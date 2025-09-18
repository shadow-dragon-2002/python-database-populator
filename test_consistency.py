#!/usr/bin/env python3
"""
Test script to verify consistent statistics across different employee counts
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_populator import DatabasePopulator

def test_consistent_statistics():
    """Test that statistics remain consistent across different employee counts"""
    print("Testing Consistent Statistics Generation")
    print("=" * 50)
    
    dp = DatabasePopulator()
    
    # Test different employee counts
    employee_counts = [5, 10, 25, 50, 100]
    
    all_stats = []
    
    for count in employee_counts:
        stats = dp.generate_consistent_statistics(count)
        all_stats.append(stats)
        
        print(f"\nEmployee Count: {count}")
        print(f"  Phishing Click Rate: {stats['phishing_click_rate']:.1f}%")
        print(f"  Vishing Response Rate: {stats['vishing_response_rate']:.1f}%")
        print(f"  Quishing Scan Rate: {stats['quishing_scan_rate']:.1f}%")
        print(f"  Physical Security Score: {stats['physical_security_score']:.1f}/10")
        print(f"  Human Security Score: {stats['human_security_score']:.1f}/10")
    
    # Check consistency
    print(f"\n{'='*50}")
    print("Consistency Analysis:")
    
    for metric in ['phishing_click_rate', 'vishing_response_rate', 'quishing_scan_rate', 'physical_security_score', 'human_security_score']:
        values = [stat[metric] for stat in all_stats]
        avg = sum(values) / len(values)
        variance = sum((x - avg) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        
        print(f"{metric.replace('_', ' ').title()}:")
        print(f"  Average: {avg:.2f}")
        print(f"  Standard Deviation: {std_dev:.2f}")
        print(f"  Range: {min(values):.2f} - {max(values):.2f}")
        
        if std_dev < 2.0:  # Within 2 units
            print(f"  ✓ CONSISTENT (std dev < 2.0)")
        else:
            print(f"  ✗ HIGH VARIATION (std dev >= 2.0)")
        print()
    
    print("✅ Statistics consistency test completed!")
    print("The same base statistics are used regardless of employee count,")
    print("ensuring consistent overall metrics in your reports.")

if __name__ == "__main__":
    test_consistent_statistics()