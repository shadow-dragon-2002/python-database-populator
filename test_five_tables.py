#!/usr/bin/env python3
"""
Test script to verify the 5 tables are created correctly and populated with data.
Tests the main database_populator.py script functionality.
"""

import sqlite3
import sys
import os
from contextlib import contextmanager

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_populator import DatabasePopulator


class SQLiteTestPopulator(DatabasePopulator):
    """SQLite version of DatabasePopulator for testing"""
    
    def __init__(self):
        super().__init__()
        self.db_type = 'sqlite'  # Use SQLite for testing
        
    def connect_to_test_database(self):
        """Connect to in-memory SQLite database for testing"""
        try:
            self.connection = sqlite3.connect(':memory:')
            self.connection.row_factory = sqlite3.Row  # Enable dict-like access
            self.cursor = self.connection.cursor()
            print("✓ Connected to in-memory SQLite database for testing")
            return True
        except Exception as e:
            print(f"✗ Failed to connect to test database: {e}")
            return False
    
    def _get_employee_master_table_sql(self):
        """SQLite version of employee_master table"""
        return """
        CREATE TABLE IF NOT EXISTS employee_master (
            serial_no INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id VARCHAR(20) UNIQUE NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            gender CHAR(1),
            date_of_birth DATE,
            age INTEGER,
            blood_group VARCHAR(5),
            marital_status VARCHAR(20),
            email VARCHAR(100),
            phone_number VARCHAR(20),
            address VARCHAR(255),
            state VARCHAR(50),
            postal_code VARCHAR(10),
            country VARCHAR(50) DEFAULT 'India',
            designation VARCHAR(50),
            department VARCHAR(50),
            salary DECIMAL(10,2),
            work_experience_years DECIMAL(4,1),
            joining_date DATE,
            emergency_contact_name VARCHAR(100),
            emergency_contact_phone VARCHAR(20),
            family_details VARCHAR(255),
            medical_conditions VARCHAR(255),
            simulation_type VARCHAR(50),
            work_email VARCHAR(100),
            personal_email VARCHAR(100),
            click_response_rate DECIMAL(5,2),
            phish_test_simulation_date DATE,
            phish_testing_status VARCHAR(20),
            vishing_phone_number VARCHAR(20),
            vishing_alt_phone_number VARCHAR(20),
            voice_auth_test BOOLEAN,
            vish_response_rate DECIMAL(5,2),
            vish_test_simulation_date DATE,
            vish_testing_status VARCHAR(20),
            branch_location VARCHAR(100),
            branch_code VARCHAR(10),
            total_employees_at_branch INTEGER,
            security_level VARCHAR(20),
            building_storeys INTEGER,
            assessment_date DATE,
            assessment_time_start TIME,
            assessment_time_end TIME,
            permission_granted BOOLEAN,
            approving_official_name VARCHAR(100),
            approving_official_designation VARCHAR(50),
            identity_verification_required BOOLEAN,
            identity_verified BOOLEAN,
            security_guard_present BOOLEAN,
            visitor_log_maintained BOOLEAN,
            badge_issued BOOLEAN,
            escort_required BOOLEAN,
            restricted_areas_accessed BOOLEAN,
            tailgating_possible BOOLEAN,
            social_engineering_successful BOOLEAN,
            physical_security_score DECIMAL(5,1),
            human_security_score DECIMAL(5,1),
            overall_assessment_score DECIMAL(5,1),
            vulnerabilities_found VARCHAR(255),
            recommendations VARCHAR(255),
            assessor_name VARCHAR(100),
            assessor_id VARCHAR(20),
            notes VARCHAR(255),
            red_team_testing_status VARCHAR(20)
        )
        """
    
    def _get_employee_phish_smish_sim_table_sql(self):
        """SQLite version of employee_phish_smish_sim table"""
        return """
        CREATE TABLE IF NOT EXISTS employee_phish_smish_sim (
            sim_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id VARCHAR(20) NOT NULL,
            simulation_type VARCHAR(50),
            work_email VARCHAR(100),
            personal_email VARCHAR(100),
            click_response_rate DECIMAL(5,2),
            testing_status VARCHAR(20),
            FOREIGN KEY (employee_id) REFERENCES employee_master(employee_id) ON DELETE CASCADE
        )
        """
    
    def _get_employee_vishing_sim_table_sql(self):
        """SQLite version of employee_vishing_sim table"""
        return """
        CREATE TABLE IF NOT EXISTS employee_vishing_sim (
            sim_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id VARCHAR(20) NOT NULL,
            phone_number VARCHAR(20),
            alt_phone_number VARCHAR(20),
            vish_response_rate DECIMAL(5,2),
            testing_status VARCHAR(20),
            FOREIGN KEY (employee_id) REFERENCES employee_master(employee_id) ON DELETE CASCADE
        )
        """
    
    def _get_employee_quishing_sim_table_sql(self):
        """SQLite version of employee_quishing_sim table"""
        return """
        CREATE TABLE IF NOT EXISTS employee_quishing_sim (
            sim_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id VARCHAR(20) NOT NULL,
            qr_code_type VARCHAR(50),
            qr_scan_rate DECIMAL(5,2),
            malicious_qr_clicked BOOLEAN,
            device_type VARCHAR(50),
            testing_status VARCHAR(20),
            simulation_date DATE,
            FOREIGN KEY (employee_id) REFERENCES employee_master(employee_id) ON DELETE CASCADE
        )
        """
    
    def _get_red_team_assessment_table_sql(self):
        """SQLite version of red_team_assessment table"""
        return """
        CREATE TABLE IF NOT EXISTS red_team_assessment (
            assess_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id VARCHAR(20) NOT NULL,
            branch_code VARCHAR(10),
            local_employees_at_branch INTEGER,
            security_level VARCHAR(20),
            building_storeys INTEGER,
            assessment_date DATE,
            assessment_time_start TIME,
            assessment_time_end TIME,
            permission_granted BOOLEAN,
            approving_official_name VARCHAR(100),
            approving_official_designation VARCHAR(50),
            identity_verification_required BOOLEAN,
            identity_verified BOOLEAN,
            security_guard_present BOOLEAN,
            visitor_log_maintained BOOLEAN,
            badge_issued BOOLEAN,
            escort_required BOOLEAN,
            restricted_areas_accessed BOOLEAN,
            tailgating_possible BOOLEAN,
            social_engineering_successful BOOLEAN,
            physical_security_score DECIMAL(5,1),
            human_security_score DECIMAL(5,1),
            overall_assessment_score DECIMAL(5,1),
            vulnerabilities_found VARCHAR(255),
            recommendations VARCHAR(255),
            assessor_name VARCHAR(100),
            assessor_id VARCHAR(20),
            notes VARCHAR(255),
            testing_status VARCHAR(20),
            FOREIGN KEY (employee_id) REFERENCES employee_master(employee_id) ON DELETE CASCADE
        )
        """


@contextmanager
def test_database_populator(num_employees):
    """Context manager for testing database populator"""
    populator = SQLiteTestPopulator()
    
    try:
        if not populator.connect_to_test_database():
            raise Exception("Could not connect to test database")
        
        if not populator.create_tables():
            raise Exception("Could not create tables")
        
        yield populator, num_employees
        
    finally:
        populator.close_connection()


def test_table_creation():
    """Test that all 5 tables are created correctly"""
    print("=== Testing Table Creation ===")
    
    with test_database_populator(10) as (populator, _):
        # Check that all 5 tables exist
        expected_tables = [
            'employee_master',
            'employee_phish_smish_sim', 
            'employee_vishing_sim',
            'employee_quishing_sim',
            'red_team_assessment'
        ]
        
        for table in expected_tables:
            populator.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            result = populator.cursor.fetchone()
            print(f"✓ Table {table} exists and accessible")
        
        print("✓ All 5 tables created successfully!")
        return True


def test_data_generation():
    """Test data generation for all tables"""
    print("\n=== Testing Data Generation ===")
    
    with test_database_populator(5) as (populator, num_employees):
        # Generate employees first
        if not populator.generate_employees(num_employees):
            print("✗ Failed to generate employees")
            return False
        
        # Get employee IDs
        employee_ids = populator.get_employee_ids()
        if not employee_ids:
            print("✗ No employee IDs found")
            return False
        
        print(f"✓ Generated {len(employee_ids)} employees")
        
        # Generate simulation data
        if not populator.generate_phish_smish_simulations(employee_ids):
            print("✗ Failed to generate phish/smish simulations")
            return False
        print("✓ Generated phish/smish simulations")
        
        if not populator.generate_vishing_simulations(employee_ids):
            print("✗ Failed to generate vishing simulations")
            return False
        print("✓ Generated vishing simulations")
        
        if not populator.generate_quishing_simulations(employee_ids):
            print("✗ Failed to generate quishing simulations")
            return False
        print("✓ Generated quishing simulations")
        
        if not populator.generate_red_team_assessments(employee_ids):
            print("✗ Failed to generate red team assessments")
            return False
        print("✓ Generated red team assessments")
        
        # Verify all tables have data
        tables = {
            'employee_master': 'employees',
            'employee_phish_smish_sim': 'phish/smish simulations',
            'employee_vishing_sim': 'vishing simulations',
            'employee_quishing_sim': 'quishing simulations',
            'red_team_assessment': 'red team assessments'
        }
        
        print("\n=== Data Verification ===")
        for table, description in tables.items():
            populator.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = populator.cursor.fetchone()[0]
            print(f"✓ {description}: {count} records")
        
        return True


def test_data_completeness():
    """Test that no required columns are empty"""
    print("\n=== Testing Data Completeness ===")
    
    with test_database_populator(3) as (populator, num_employees):
        # Generate data
        if not populator.generate_employees(num_employees):
            return False
        
        employee_ids = populator.get_employee_ids()
        populator.generate_phish_smish_simulations(employee_ids)
        populator.generate_vishing_simulations(employee_ids)
        populator.generate_quishing_simulations(employee_ids)
        populator.generate_red_team_assessments(employee_ids)
        
        # Check for empty required fields in employee_master
        required_fields = [
            'employee_id', 'first_name', 'last_name', 'email', 
            'phone_number', 'department', 'designation'
        ]
        
        for field in required_fields:
            populator.cursor.execute(f"""
                SELECT COUNT(*) FROM employee_master 
                WHERE {field} IS NULL OR {field} = ''
            """)
            null_count = populator.cursor.fetchone()[0]
            if null_count > 0:
                print(f"✗ Found {null_count} empty {field} values")
                return False
            else:
                print(f"✓ No empty {field} values found")
        
        print("✓ All required fields are properly filled!")
        return True


def main():
    """Run all tests"""
    print("Five Tables Database Populator Test")
    print("=" * 50)
    
    tests = [
        test_table_creation,
        test_data_generation,
        test_data_completeness
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"✗ Test {test.__name__} failed")
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
    
    print(f"\n=== Test Summary ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The 5 tables are working correctly.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total


if __name__ == "__main__":
    main()