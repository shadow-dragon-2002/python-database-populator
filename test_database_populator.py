#!/usr/bin/env python3
"""
Simple test script to validate database_populator functionality
without requiring actual database connections.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_populator import DatabasePopulator, IndianDataProvider, get_yes_no_input
from faker import Faker
import unittest
from unittest.mock import patch, MagicMock


class TestDatabasePopulator(unittest.TestCase):
    """Test cases for DatabasePopulator functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.populator = DatabasePopulator()
    
    def test_indian_data_provider(self):
        """Test Indian data provider generates expected data"""
        fake = Faker()
        fake.add_provider(IndianDataProvider)
        
        # Test Indian name generation
        name = fake.indian_name()
        self.assertIsInstance(name, str)
        self.assertIn(' ', name)  # Should have first and last name
        
        # Test Indian phone generation
        phone = fake.indian_phone()
        self.assertIsInstance(phone, str)
        self.assertTrue(phone.startswith('+91'))
        
        # Test Indian city generation
        city = fake.indian_city()
        self.assertIsInstance(city, str)
        self.assertIn(city, IndianDataProvider.indian_cities)
    
    def test_database_type_validation(self):
        """Test database type is set correctly"""
        self.populator.db_type = 'mysql'
        self.assertEqual(self.populator.db_type, 'mysql')
        
        self.populator.db_type = 'postgresql'
        self.assertEqual(self.populator.db_type, 'postgresql')
    
    def test_table_sql_generation(self):
        """Test SQL generation for different database types"""
        # Test MySQL SQL generation
        self.populator.db_type = 'mysql'
        employees_sql = self.populator._get_employee_master_table_sql()
        self.assertIn('AUTO_INCREMENT', employees_sql)
        self.assertIn('ENGINE=InnoDB', employees_sql)
        
        # Test PostgreSQL SQL generation
        self.populator.db_type = 'postgresql'
        employees_sql = self.populator._get_employee_master_table_sql()
        self.assertIn('SERIAL', employees_sql)
        self.assertIn('employee_id INT UNIQUE', employees_sql)
    
    def test_get_yes_no_input_mock(self):
        """Test yes/no input function with mocked input"""
        with patch('builtins.input', return_value='yes'):
            result = get_yes_no_input("Test prompt")
            self.assertTrue(result)
        
        with patch('builtins.input', return_value='no'):
            result = get_yes_no_input("Test prompt")
            self.assertFalse(result)
        
        with patch('builtins.input', return_value='y'):
            result = get_yes_no_input("Test prompt")
            self.assertTrue(result)
        
        with patch('builtins.input', return_value='n'):
            result = get_yes_no_input("Test prompt")
            self.assertFalse(result)


def test_data_generation():
    """Test data generation without database connection"""
    print("Testing data generation logic...")
    
    populator = DatabasePopulator()
    
    # Test employee data structure
    fake = populator.fake
    
    departments = ['IT Security', 'Human Resources', 'Finance', 'Operations', 'Marketing', 'Sales']
    positions = ['Analyst', 'Manager', 'Coordinator', 'Specialist', 'Executive', 'Director']
    
    print("Sample employee data:")
    for i in range(3):
        employee_id = f"FISST{str(i+1).zfill(4)}"
        name = fake.indian_name()
        email = f"{name.lower().replace(' ', '.')}@fisst.edu"
        phone = fake.indian_phone()
        city = fake.indian_city()
        
        print(f"  {employee_id}: {name}, {email}, {phone}, {city}")
    
    print("✓ Employee data generation test passed!")


def main():
    """Run all tests"""
    print("Running Database Populator Tests")
    print("=" * 40)
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run additional tests
    test_data_generation()
    
    print("\n" + "=" * 40)
    print("All tests completed!")


if __name__ == "__main__":
    main()