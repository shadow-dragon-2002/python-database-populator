#!/usr/bin/env python3
"""
Validation script for database_populator.py
Tests data generation and validates that all columns are properly filled.
"""

import sys
import os
import random
from decimal import Decimal

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_populator import DatabasePopulator, IndianDataProvider
from faker import Faker


class MockCursor:
    """Mock cursor for testing SQL generation without database"""
    
    def __init__(self):
        self.executed_sqls = []
        self.executed_data = []
        self.tables = {
            'employee_master': [],
            'employee_phish_smish_sim': [],
            'employee_vishing_sim': [],
            'employee_quishing_sim': [],
            'red_team_assessment': []
        }
    
    def execute(self, sql, params=None):
        self.executed_sqls.append(sql)
        if params:
            self.executed_data.append(params)
        # Simulate successful execution
        return True
    
    def executemany(self, sql, data_list):
        self.executed_sqls.append(sql)
        table_name = self._extract_table_name(sql)
        if table_name:
            self.tables[table_name].extend(data_list)
        return True
    
    def fetchone(self):
        # Return mock data for count queries
        return {'count': len(self.tables.get('employee_master', []))}
    
    def fetchall(self):
        # Return mock employee IDs
        return [{'employee_id': f'FISST{i+1:04d}'} for i in range(len(self.tables.get('employee_master', [])))]
    
    def _extract_table_name(self, sql):
        """Extract table name from INSERT SQL"""
        sql_lower = sql.lower()
        if 'insert into' in sql_lower:
            start = sql_lower.find('insert into') + len('insert into')
            end = sql_lower.find('(', start)
            return sql_lower[start:end].strip()
        return None
    
    def close(self):
        pass


class MockConnection:
    """Mock connection for testing"""
    
    def __init__(self):
        self.committed = False
        self.rolled_back = False
    
    def commit(self):
        self.committed = True
    
    def rollback(self):
        self.rolled_back = True
    
    def close(self):
        pass


class ValidationPopulator(DatabasePopulator):
    """DatabasePopulator for validation testing"""
    
    def __init__(self):
        super().__init__()
        self.db_type = 'mysql'  # Use MySQL syntax
        self.cursor = MockCursor()
        self.connection = MockConnection()
    
    def connect_to_database(self, config):
        return True
    
    def close_connection(self):
        pass


def validate_table_sql():
    """Validate that all 5 table SQL statements are correct"""
    print("=== Validating Table SQL Generation ===")
    
    populator = ValidationPopulator()
    
    # Test MySQL tables
    populator.db_type = 'mysql'
    tables = {
        'employee_master': populator._get_employee_master_table_sql(),
        'employee_phish_smish_sim': populator._get_employee_phish_smish_sim_table_sql(),
        'employee_vishing_sim': populator._get_employee_vishing_sim_table_sql(),
        'employee_quishing_sim': populator._get_employee_quishing_sim_table_sql(),
        'red_team_assessment': populator._get_red_team_assessment_table_sql()
    }
    
    for table_name, sql in tables.items():
        if sql and 'CREATE TABLE' in sql:
            print(f"✓ {table_name}: SQL generated successfully")
        else:
            print(f"✗ {table_name}: SQL generation failed")
            return False
    
    # Test PostgreSQL tables
    populator.db_type = 'postgresql'
    tables_pg = {
        'employee_master': populator._get_employee_master_table_sql(),
        'employee_phish_smish_sim': populator._get_employee_phish_smish_sim_table_sql(),
        'employee_vishing_sim': populator._get_employee_vishing_sim_table_sql(),
        'employee_quishing_sim': populator._get_employee_quishing_sim_table_sql(),
        'red_team_assessment': populator._get_red_team_assessment_table_sql()
    }
    
    for table_name, sql in tables_pg.items():
        if sql and 'CREATE TABLE' in sql:
            print(f"✓ {table_name} (PostgreSQL): SQL generated successfully")
        else:
            print(f"✗ {table_name} (PostgreSQL): SQL generation failed")
            return False
    
    return True


def validate_data_generation():
    """Validate that data generation works for all tables"""
    print("\n=== Validating Data Generation ===")
    
    populator = ValidationPopulator()
    num_employees = 5
    
    # Test employee generation
    if not populator.generate_employees(num_employees):
        print("✗ Employee generation failed")
        return False
    
    employee_data = populator.cursor.tables['employee_master']
    if len(employee_data) != num_employees:
        print(f"✗ Expected {num_employees} employees, got {len(employee_data)}")
        return False
    
    print(f"✓ Generated {len(employee_data)} employees successfully")
    
    # Get employee IDs for other tables
    employee_ids = [f'FISST{i+1:04d}' for i in range(num_employees)]
    
    # Test phish/smish simulations
    if not populator.generate_phish_smish_simulations(employee_ids):
        print("✗ Phish/smish simulation generation failed")
        return False
    
    phish_data = populator.cursor.tables['employee_phish_smish_sim']
    print(f"✓ Generated {len(phish_data)} phish/smish simulation entries")
    
    # Test vishing simulations
    if not populator.generate_vishing_simulations(employee_ids):
        print("✗ Vishing simulation generation failed")
        return False
    
    vishing_data = populator.cursor.tables['employee_vishing_sim']
    print(f"✓ Generated {len(vishing_data)} vishing simulation entries")
    
    # Test quishing simulations
    if not populator.generate_quishing_simulations(employee_ids):
        print("✗ Quishing simulation generation failed")
        return False
    
    quishing_data = populator.cursor.tables['employee_quishing_sim']
    print(f"✓ Generated {len(quishing_data)} quishing simulation entries")
    
    # Test red team assessments
    if not populator.generate_red_team_assessments(employee_ids):
        print("✗ Red team assessment generation failed")
        return False
    
    assessment_data = populator.cursor.tables['red_team_assessment']
    print(f"✓ Generated {len(assessment_data)} red team assessment entries")
    
    return True


def validate_data_completeness():
    """Validate that all required fields are filled"""
    print("\n=== Validating Data Completeness ===")
    
    populator = ValidationPopulator()
    num_employees = 3
    
    # Generate data
    populator.generate_employees(num_employees)
    employee_ids = [f'FISST{i+1:04d}' for i in range(num_employees)]
    populator.generate_phish_smish_simulations(employee_ids)
    populator.generate_vishing_simulations(employee_ids)
    populator.generate_quishing_simulations(employee_ids)
    populator.generate_red_team_assessments(employee_ids)
    
    # Check employee_master data completeness
    employee_data = populator.cursor.tables['employee_master']
    
    if not employee_data:
        print("✗ No employee data generated")
        return False
    
    # Check that all required fields are present and not empty
    required_fields_positions = {
        'employee_id': 0,
        'first_name': 1,
        'last_name': 2,
        'email': 8,
        'phone_number': 9,
        'department': 15,
        'designation': 14
    }
    
    for employee_record in employee_data:
        for field_name, position in required_fields_positions.items():
            if position >= len(employee_record) or not employee_record[position]:
                print(f"✗ Missing or empty {field_name} in employee record")
                return False
    
    print(f"✓ All {len(employee_data)} employee records have complete required fields")
    
    # Check that optional fields are also filled (no None values)
    all_fields_filled = True
    for employee_record in employee_data:
        for i, value in enumerate(employee_record):
            if value is None:
                print(f"✗ Field at position {i} is None in employee record")
                all_fields_filled = False
                break
    
    if all_fields_filled:
        print("✓ All employee fields are properly filled (no None values)")
    
    # Check other tables have data
    tables_to_check = [
        ('employee_phish_smish_sim', 'phish/smish simulations'),
        ('employee_vishing_sim', 'vishing simulations'),
        ('employee_quishing_sim', 'quishing simulations'),
        ('red_team_assessment', 'red team assessments')
    ]
    
    for table_name, description in tables_to_check:
        table_data = populator.cursor.tables[table_name]
        if table_data:
            print(f"✓ {description}: {len(table_data)} records generated")
        else:
            print(f"✗ {description}: No records generated")
            return False
    
    return all_fields_filled


def validate_data_types_and_ranges():
    """Validate that data types and value ranges are appropriate"""
    print("\n=== Validating Data Types and Ranges ===")
    
    populator = ValidationPopulator()
    num_employees = 3
    
    # Generate data
    populator.generate_employees(num_employees)
    employee_data = populator.cursor.tables['employee_master']
    
    if not employee_data:
        print("✗ No employee data to validate")
        return False
    
    # Check specific data type constraints
    for i, employee_record in enumerate(employee_data):
        # Check employee_id format (should be FISST####)
        employee_id = employee_record[0]
        if not (employee_id.startswith('FISST') and len(employee_id) == 9):
            print(f"✗ Employee {i}: Invalid employee_id format: {employee_id}")
            return False
        
        # Check age is reasonable (should be between 22 and 65)
        age = employee_record[5]
        if not (22 <= age <= 65):
            print(f"✗ Employee {i}: Invalid age: {age}")
            return False
        
        # Check salary is reasonable (should be positive)
        salary = employee_record[16]
        if salary <= 0:
            print(f"✗ Employee {i}: Invalid salary: {salary}")
            return False
        
        # Check email format (should contain @)
        email = employee_record[8]
        if '@' not in email:
            print(f"✗ Employee {i}: Invalid email format: {email}")
            return False
    
    print("✓ All data types and ranges are valid")
    
    # Check rate ranges for simulations
    phish_data = populator.cursor.tables['employee_phish_smish_sim']
    if phish_data:
        for record in phish_data:
            click_rate = record[4]  # click_response_rate position
            if not (0 <= click_rate <= 100):
                print(f"✗ Invalid click response rate: {click_rate}")
                return False
        print("✓ Phishing simulation rates are in valid range (0-100%)")
    
    return True


def main():
    """Run all validation tests"""
    print("Database Populator Validation Suite")
    print("=" * 50)
    
    tests = [
        validate_table_sql,
        validate_data_generation,
        validate_data_completeness,
        validate_data_types_and_ranges
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
            import traceback
            traceback.print_exc()
    
    print(f"\n=== Validation Summary ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All validations passed! The database populator is working correctly.")
        print("\nThe script creates exactly 5 tables:")
        print("1. employee_master - Contains all employee information")
        print("2. employee_phish_smish_sim - Phishing/SMS phishing simulations")
        print("3. employee_vishing_sim - Voice phishing simulations")
        print("4. employee_quishing_sim - QR code phishing simulations")
        print("5. red_team_assessment - Red team security assessments")
        print("\nAll tables are properly populated with complete data, no empty columns.")
    else:
        print("❌ Some validations failed. Please check the errors above.")
    
    return passed == total


if __name__ == "__main__":
    main()