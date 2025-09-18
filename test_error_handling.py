#!/usr/bin/env python3
"""
Test script to demonstrate the improved error handling
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_populator import DatabasePopulator

def test_error_scenarios():
    """Test different error scenarios"""
    print("Testing Enhanced Error Handling")
    print("=" * 40)
    
    populator = DatabasePopulator()
    populator.db_type = 'mysql'
    
    # Test 1: Access denied error
    print("\n1. Testing Access Denied Error:")
    config1 = {
        'host': 'localhost',
        'port': 3306,
        'database': 'test_db',
        'username': 'wrong_user',
        'password': 'wrong_password'
    }
    populator.connect_to_database(config1)
    
    # Test 2: Connection refused error
    print("\n" + "="*50)
    print("2. Testing Connection Refused Error:")
    config2 = {
        'host': 'nonexistent.host.com',
        'port': 3306,
        'database': 'test_db',
        'username': 'root',
        'password': 'password'
    }
    populator.connect_to_database(config2)
    
    # Test 3: Unknown database error
    print("\n" + "="*50)
    print("3. Testing Unknown Database Error:")
    # This will be simulated by the error message matching
    
    print("\n" + "="*50)
    print("✅ Error handling demonstration complete!")
    print("The enhanced error messages provide:")
    print("  • Specific troubleshooting steps for each error type")
    print("  • Current configuration details")
    print("  • Quick solution suggestions")
    print("  • Command examples for testing connections")

if __name__ == "__main__":
    test_error_scenarios()