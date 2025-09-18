#!/usr/bin/env python3
"""
Debug script to test the exact scenario shown in the user's image
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_populator import DatabasePopulator

def debug_method_availability():
    """Debug method availability at different stages"""
    print("=== Debugging Method Availability ===")
    
    # Test 1: Fresh instance
    print("\n1. Testing fresh DatabasePopulator instance:")
    dp = DatabasePopulator()
    print(f"   - Has _get_red_team_assessment_table_sql: {hasattr(dp, '_get_red_team_assessment_table_sql')}")
    
    # Test 2: Set db_type
    print("\n2. After setting db_type to mysql:")
    dp.db_type = 'mysql'
    print(f"   - Has _get_red_team_assessment_table_sql: {hasattr(dp, '_get_red_team_assessment_table_sql')}")
    
    # Test 3: Try calling the method
    print("\n3. Trying to call the method:")
    try:
        result = dp._get_red_team_assessment_table_sql()
        print(f"   - Method call successful, result length: {len(result)}")
        print(f"   - Contains CREATE TABLE: {'CREATE TABLE' in result}")
    except Exception as e:
        print(f"   - Error calling method: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Test create_tables method
    print("\n4. Testing create_tables method (without database connection):")
    try:
        # Mock connection and cursor
        class MockCursor:
            def execute(self, sql):
                print(f"     - Would execute SQL of length: {len(sql)}")
                
        class MockConnection:
            def commit(self):
                print("     - Would commit")
            def rollback(self):
                print("     - Would rollback")
        
        dp.cursor = MockCursor()
        dp.connection = MockConnection()
        
        # This should show us if all methods are callable during table creation
        tables = {
            'employee_master': dp._get_employee_master_table_sql(),
            'employee_phish_smish_sim': dp._get_employee_phish_smish_sim_table_sql(),
            'employee_vishing_sim': dp._get_employee_vishing_sim_table_sql(),
            'employee_quishing_sim': dp._get_employee_quishing_sim_table_sql(),
            'red_team_assessment': dp._get_red_team_assessment_table_sql()
        }
        print("   - All table SQL methods callable successfully!")
        
        for table_name, sql in tables.items():
            dp.cursor.execute(sql)
            print(f"     ✓ Would create table: {table_name}")
        
        print("   - create_tables simulation successful!")
        
    except Exception as e:
        print(f"   - Error in create_tables simulation: {e}")
        import traceback
        traceback.print_exc()

def test_exact_user_scenario():
    """Test the exact scenario from user's image"""
    print("\n=== Testing Exact User Scenario ===")
    print("Simulating: mysql connection to localhost with successful connection...")
    
    dp = DatabasePopulator()
    dp.db_type = 'mysql'
    
    # Simulate successful connection
    print("✓ Successfully connected to mysql database!")
    
    # Mock the connection objects to simulate real scenario
    class MockCursor:
        def execute(self, sql):
            if len(sql) > 100:  # Table creation SQL
                print(f"Executing CREATE TABLE... (length: {len(sql)})")
            else:
                print(f"Executing: {sql}")
    
    class MockConnection:
        def commit(self):
            pass
        def rollback(self):
            pass
    
    dp.cursor = MockCursor()
    dp.connection = MockConnection()
    
    # This is where the error occurs according to the image
    print("\n📋 Creating database tables...")
    try:
        # This simulates the exact call that's failing
        result = dp.create_tables()
        print(f"create_tables result: {result}")
    except Exception as e:
        print(f"❌ Error during table creation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_method_availability()
    test_exact_user_scenario()