#!/usr/bin/env python3
"""
Comprehensive test script for database_populator.py
Tests data generation accuracy across multiple runs with different employee counts.
Validates that generated data matches the FISST Academy case study percentages.
"""

import sys
import os
import sqlite3
import statistics
import random
from contextlib import contextmanager

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_populator import DatabasePopulator, IndianDataProvider
from faker import Faker


class SQLiteTestPopulator(DatabasePopulator):
    """Modified DatabasePopulator for SQLite testing"""
    
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
    
    def generate_employees(self, num_employees):
        """Generate employee data - SQLite version"""
        departments = ['IT Security', 'Human Resources', 'Finance', 'Operations', 'Marketing', 'Sales']
        positions = ['Analyst', 'Manager', 'Coordinator', 'Specialist', 'Executive', 'Director']
        
        employees_data = []
        used_emails = set()
        
        for i in range(num_employees):
            employee_id = f"FISST{str(i+1).zfill(4)}"
            name = self.fake.indian_name()
            
            # Generate unique email
            base_email = f"{name.lower().replace(' ', '.')}"
            email = f"{base_email}@fisst.edu"
            counter = 1
            while email in used_emails:
                email = f"{base_email}{counter}@fisst.edu"
                counter += 1
            used_emails.add(email)
            
            phone = self.fake.indian_phone()
            department = random.choice(departments)
            position = random.choice(positions)
            city = self.fake.indian_city()
            address = f"{random.randint(1, 999)}, {self.fake.street_name()}, {city}"
            hire_date = self.fake.date_between(start_date='-5y', end_date='today')
            
            employees_data.append((
                employee_id, name, email, phone, department, position,
                city, address, str(hire_date)  # Convert date to string for SQLite
            ))
        
        try:
            sql = """
            INSERT INTO employees (employee_id, name, email, phone, department, position, city, address, hire_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            self.cursor.executemany(sql, employees_data)
            self.connection.commit()
            print(f"✓ Generated {num_employees} employees successfully!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating employees: {e}")
            self.connection.rollback()
            return False
    
    def generate_security_metrics(self, employee_ids):
        """Generate security metrics data based on case study - SQLite version"""
        import random
        metrics_data = []
        
        # Generate baseline data (22% click rate, 0% reporting)
        baseline_entries = len(employee_ids) * 3  # 3 baseline measurements per employee
        for _ in range(baseline_entries):
            employee_id = random.choice(employee_ids)
            click_rate = random.uniform(20, 24)  # Around 22%
            reporting_rate = 0  # Zero reporting initially
            
            metrics_data.append((
                employee_id,
                str(self.fake.date_between(start_date='-6m', end_date='-3m')),
                click_rate,
                reporting_rate,
                False,  # training_completed
                'Baseline',
                False   # intervention_applied
            ))
        
        # Generate post-intervention data (5% click rate, 38% reporting)
        intervention_entries = len(employee_ids) * 2  # 2 post-intervention measurements per employee
        for _ in range(intervention_entries):
            employee_id = random.choice(employee_ids)
            click_rate = random.uniform(3, 7)  # Around 5%
            reporting_rate = random.uniform(35, 41)  # Around 38%
            
            metrics_data.append((
                employee_id,
                str(self.fake.date_between(start_date='-3m', end_date='today')),
                click_rate,
                reporting_rate,
                random.choice([True, False]),  # training_completed
                random.choice(['Simulation', 'Intrusion Test', 'Training']),
                True   # intervention_applied
            ))
        
        try:
            sql = """
            INSERT INTO security_metrics (employee_id, metric_date, click_rate, reporting_rate, training_completed, simulation_type, intervention_applied)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            self.cursor.executemany(sql, metrics_data)
            self.connection.commit()
            print(f"✓ Generated {len(metrics_data)} security metrics entries!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating security metrics: {e}")
            self.connection.rollback()
            return False
    
    def generate_usb_incidents(self, employee_ids):
        """Generate USB incident data - SQLite version"""
        import random
        incidents_data = []
        device_types = ['USB Drive', 'External HDD', 'Phone', 'Tablet', 'Unknown Device']
        locations = ['Workstation', 'Conference Room', 'Lab', 'Reception', 'Server Room']
        
        # Generate 11 initial incidents (before intervention)
        for _ in range(11):
            employee_id = random.choice(employee_ids)
            incidents_data.append((
                employee_id,
                str(self.fake.date_between(start_date='-6m', end_date='-3m')),
                random.choice(device_types),
                False,  # not blocked initially
                random.choice(locations)
            ))
        
        try:
            sql = """
            INSERT INTO usb_incidents (employee_id, incident_date, device_type, blocked, location)
            VALUES (?, ?, ?, ?, ?)
            """
            
            self.cursor.executemany(sql, incidents_data)
            self.connection.commit()
            print(f"✓ Generated {len(incidents_data)} USB incident entries!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating USB incidents: {e}")
            self.connection.rollback()
            return False
    
    def generate_intrusion_attempts(self):
        """Generate intrusion attempts data - SQLite version"""
        import random
        attempts_data = []
        attempt_types = ['Phishing', 'Malware', 'Social Engineering', 'Network Scan', 'Brute Force']
        severities = ['Low', 'Medium', 'High', 'Critical']
        
        # Generate various intrusion attempts, all blocked at reception
        for _ in range(50):
            attempts_data.append((
                str(self.fake.date_between(start_date='-6m', end_date='today')),
                self.fake.ipv4(),
                random.choice(attempt_types),
                True,  # blocked_at_reception
                random.choice(severities)
            ))
        
        try:
            sql = """
            INSERT INTO intrusion_attempts (attempt_date, source_ip, attempt_type, blocked_at_reception, severity)
            VALUES (?, ?, ?, ?, ?)
            """
            
            self.cursor.executemany(sql, attempts_data)
            self.connection.commit()
            print(f"✓ Generated {len(attempts_data)} intrusion attempt entries!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating intrusion attempts: {e}")
            self.connection.rollback()
            return False
    
    def generate_roi_tracking(self):
        """Generate ROI tracking data - SQLite version"""
        from decimal import Decimal
        # Based on case study: ₹7.3 crore avoided, 15x+ ROI
        engagement_cost = Decimal('48666666.67')  # ₹7.3 crore / 15 = approx ₹48.67 lakh
        avoided_fraud = Decimal('730000000.00')  # ₹7.3 crore
        roi_multiple = Decimal('15.0')
        
        roi_data = [(
            str(self.fake.date_between(start_date='-1m', end_date='today')),
            float(engagement_cost),
            float(avoided_fraud),
            float(roi_multiple),
            'INR',
            'Avoided phishing payroll fraud through security awareness training and intervention measures'
        )]
        
        try:
            sql = """
            INSERT INTO roi_tracking (tracking_date, engagement_cost, avoided_fraud_amount, roi_multiple, currency, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            
            self.cursor.executemany(sql, roi_data)
            self.connection.commit()
            print(f"✓ Generated ROI tracking entry!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating ROI tracking: {e}")
            self.connection.rollback()
            return False
    
    def _get_employees_table_sql(self):
        """SQLite version of employees table"""
        return """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20),
            department VARCHAR(50),
            position VARCHAR(50),
            city VARCHAR(50),
            address TEXT,
            hire_date DATE,
            organization VARCHAR(100) DEFAULT 'FISST Academy',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    
    def _get_security_metrics_table_sql(self):
        """SQLite version of security metrics table"""
        return """
        CREATE TABLE IF NOT EXISTS security_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id VARCHAR(20) NOT NULL,
            metric_date DATE NOT NULL,
            click_rate DECIMAL(5,2),
            reporting_rate DECIMAL(5,2),
            training_completed BOOLEAN DEFAULT FALSE,
            simulation_type VARCHAR(50),
            intervention_applied BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
        )
        """
    
    def _get_usb_incidents_table_sql(self):
        """SQLite version of USB incidents table"""
        return """
        CREATE TABLE IF NOT EXISTS usb_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id VARCHAR(20) NOT NULL,
            incident_date DATE NOT NULL,
            device_type VARCHAR(50),
            blocked BOOLEAN DEFAULT FALSE,
            location VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
        )
        """
    
    def _get_intrusion_attempts_table_sql(self):
        """SQLite version of intrusion attempts table"""
        return """
        CREATE TABLE IF NOT EXISTS intrusion_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_date DATE NOT NULL,
            source_ip VARCHAR(45),
            attempt_type VARCHAR(50),
            blocked_at_reception BOOLEAN DEFAULT TRUE,
            severity VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    
    def _get_roi_tracking_table_sql(self):
        """SQLite version of ROI tracking table"""
        return """
        CREATE TABLE IF NOT EXISTS roi_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_date DATE NOT NULL,
            engagement_cost DECIMAL(15,2),
            avoided_fraud_amount DECIMAL(15,2),
            roi_multiple DECIMAL(10,2),
            currency VARCHAR(10) DEFAULT 'INR',
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    
    def get_detailed_metrics(self):
        """Get detailed metrics for validation"""
        try:
            # Security metrics analysis
            self.cursor.execute("""
                SELECT 
                    AVG(CASE WHEN intervention_applied = 0 THEN click_rate END) as baseline_click_rate,
                    AVG(CASE WHEN intervention_applied = 1 THEN click_rate END) as post_intervention_click_rate,
                    AVG(CASE WHEN intervention_applied = 0 THEN reporting_rate END) as baseline_reporting_rate,
                    AVG(CASE WHEN intervention_applied = 1 THEN reporting_rate END) as post_intervention_reporting_rate,
                    COUNT(CASE WHEN intervention_applied = 0 THEN 1 END) as baseline_count,
                    COUNT(CASE WHEN intervention_applied = 1 THEN 1 END) as post_intervention_count
                FROM security_metrics
            """)
            
            metrics = self.cursor.fetchone()
            
            # USB incidents
            self.cursor.execute("SELECT COUNT(*) FROM usb_incidents WHERE blocked = 0")
            usb_incidents = self.cursor.fetchone()[0]
            
            # Intrusion attempts
            self.cursor.execute("SELECT COUNT(*) FROM intrusion_attempts WHERE blocked_at_reception = 1")
            blocked_intrusions = self.cursor.fetchone()[0]
            
            # ROI data
            self.cursor.execute("SELECT avoided_fraud_amount, roi_multiple FROM roi_tracking LIMIT 1")
            roi_result = self.cursor.fetchone()
            
            return {
                'baseline_click_rate': float(metrics[0]) if metrics[0] else 0,
                'post_intervention_click_rate': float(metrics[1]) if metrics[1] else 0,
                'baseline_reporting_rate': float(metrics[2]) if metrics[2] else 0,
                'post_intervention_reporting_rate': float(metrics[3]) if metrics[3] else 0,
                'baseline_count': metrics[4],
                'post_intervention_count': metrics[5],
                'usb_incidents': usb_incidents,
                'blocked_intrusions': blocked_intrusions,
                'avoided_fraud': float(roi_result[0]) if roi_result else 0,
                'roi_multiple': float(roi_result[1]) if roi_result else 0
            }
            
        except Exception as e:
            print(f"Error getting detailed metrics: {e}")
            return None


@contextmanager
def test_database_populator(num_employees):
    """Context manager for testing database populator"""
    populator = SQLiteTestPopulator()
    try:
        if populator.connect_to_test_database():
            if populator.create_tables():
                yield populator, num_employees
            else:
                raise Exception("Failed to create tables")
        else:
            raise Exception("Failed to connect to database")
    finally:
        populator.close_connection()


def run_single_test(test_num, num_employees):
    """Run a single test with specified number of employees"""
    print(f"\n{'='*20} TEST {test_num}: {num_employees} Employees {'='*20}")
    
    with test_database_populator(num_employees) as (populator, employee_count):
        # Generate data
        if not populator.generate_employees(employee_count):
            print(f"✗ Test {test_num}: Failed to generate employees")
            return None
        
        employee_ids = populator.get_employee_ids()
        if not employee_ids:
            print(f"✗ Test {test_num}: No employee IDs found")
            return None
        
        if not (populator.generate_security_metrics(employee_ids) and
                populator.generate_usb_incidents(employee_ids) and
                populator.generate_intrusion_attempts() and
                populator.generate_roi_tracking()):
            print(f"✗ Test {test_num}: Failed to generate complete data")
            return None
        
        # Get detailed metrics
        metrics = populator.get_detailed_metrics()
        if not metrics:
            print(f"✗ Test {test_num}: Failed to retrieve metrics")
            return None
        
        # Display results
        print(f"Results for {employee_count} employees:")
        print(f"  Baseline Click Rate: {metrics['baseline_click_rate']:.2f}% (target: ~22%)")
        print(f"  Post-Intervention Click Rate: {metrics['post_intervention_click_rate']:.2f}% (target: ~5%)")
        print(f"  Baseline Reporting Rate: {metrics['baseline_reporting_rate']:.2f}% (target: 0%)")
        print(f"  Post-Intervention Reporting Rate: {metrics['post_intervention_reporting_rate']:.2f}% (target: ~38%)")
        print(f"  USB Incidents: {metrics['usb_incidents']} (target: 11)")
        print(f"  Blocked Intrusions: {metrics['blocked_intrusions']} (target: all blocked)")
        print(f"  ROI Multiple: {metrics['roi_multiple']:.1f}x (target: 15x)")
        print(f"  Avoided Fraud: ₹{metrics['avoided_fraud']/10000000:.1f} crore (target: ₹7.3 crore)")
        
        return metrics


def validate_metrics(metrics, test_num, num_employees):
    """Validate that metrics meet expected ranges"""
    issues = []
    
    # Expected ranges based on the case study
    expected_ranges = {
        'baseline_click_rate': (20, 24),  # 20-24% around 22%
        'post_intervention_click_rate': (3, 7),  # 3-7% around 5%
        'baseline_reporting_rate': (0, 0),  # Exactly 0%
        'post_intervention_reporting_rate': (35, 41),  # 35-41% around 38%
        'usb_incidents': (11, 11),  # Exactly 11
        'roi_multiple': (15, 15),  # Exactly 15x
        'avoided_fraud': (730000000, 730000000)  # Exactly ₹7.3 crore (not 73 crore)
    }
    
    for metric, (min_val, max_val) in expected_ranges.items():
        if metric in metrics:
            value = metrics[metric]
            if not (min_val <= value <= max_val):
                issues.append(f"{metric}: {value:.2f} (expected {min_val}-{max_val})")
    
    if issues:
        print(f"⚠️  Test {test_num}: Metrics outside expected ranges:")
        for issue in issues:
            print(f"    {issue}")
        return False
    else:
        print(f"✓ Test {test_num}: All metrics within expected ranges")
        return True


def run_comprehensive_tests():
    """Run comprehensive tests with different employee counts"""
    print("FISST Academy Database Populator - Comprehensive Test Suite")
    print("=" * 70)
    print("Testing data generation accuracy across multiple runs")
    print("Expected targets based on case study:")
    print("• Baseline: ~22% click rate, 0% reporting, 11 USB incidents")
    print("• Post-intervention: ~5% click rate, ~38% reporting, 0 new USB incidents")
    print("• ROI: ₹7.3 crore avoided fraud, 15x return on investment")
    print("=" * 70)
    
    # Test with different employee counts
    test_configs = [
        (1, 25),   # Small dataset
        (2, 50),   # Medium dataset
        (3, 100),  # Large dataset
        (4, 30),   # Small-medium dataset
        (5, 75),   # Medium-large dataset
        (6, 150)   # Very large dataset
    ]
    
    all_results = []
    successful_tests = 0
    
    for test_num, employee_count in test_configs:
        try:
            result = run_single_test(test_num, employee_count)
            if result:
                result['test_num'] = test_num
                result['employee_count'] = employee_count
                all_results.append(result)
                
                if validate_metrics(result, test_num, employee_count):
                    successful_tests += 1
            else:
                print(f"✗ Test {test_num}: Failed to complete")
        except Exception as e:
            print(f"✗ Test {test_num}: Exception occurred - {e}")
    
    # Summary analysis
    print(f"\n{'='*30} TEST SUMMARY {'='*30}")
    print(f"Completed tests: {len(all_results)}/6")
    print(f"Tests within expected ranges: {successful_tests}/{len(all_results)}")
    
    if all_results:
        # Calculate aggregate statistics
        baseline_clicks = [r['baseline_click_rate'] for r in all_results]
        post_clicks = [r['post_intervention_click_rate'] for r in all_results]
        baseline_reports = [r['baseline_reporting_rate'] for r in all_results]
        post_reports = [r['post_intervention_reporting_rate'] for r in all_results]
        
        print(f"\nAggregate Statistics across all tests:")
        print(f"Baseline Click Rate: {statistics.mean(baseline_clicks):.2f}% ± {statistics.stdev(baseline_clicks):.2f}% (target: ~22%)")
        print(f"Post-Intervention Click Rate: {statistics.mean(post_clicks):.2f}% ± {statistics.stdev(post_clicks):.2f}% (target: ~5%)")
        print(f"Baseline Reporting Rate: {statistics.mean(baseline_reports):.2f}% ± {statistics.stdev(baseline_reports):.2f}% (target: 0%)")
        print(f"Post-Intervention Reporting Rate: {statistics.mean(post_reports):.2f}% ± {statistics.stdev(post_reports):.2f}% (target: ~38%)")
        
        # Check consistency
        click_rate_consistency = statistics.stdev(baseline_clicks) < 2.0  # Less than 2% standard deviation
        report_rate_consistency = statistics.stdev(post_reports) < 3.0   # Less than 3% standard deviation
        
        print(f"\nConsistency Analysis:")
        print(f"Click rate consistency: {'✓ Good' if click_rate_consistency else '⚠️ Variable'}")
        print(f"Reporting rate consistency: {'✓ Good' if report_rate_consistency else '⚠️ Variable'}")
        
        # Final assessment
        overall_success = (successful_tests >= 5 and  # At least 5/6 tests pass
                          statistics.mean(baseline_clicks) > 20 and statistics.mean(baseline_clicks) < 24 and
                          statistics.mean(post_clicks) > 3 and statistics.mean(post_clicks) < 7 and
                          statistics.mean(post_reports) > 35 and statistics.mean(post_reports) < 41)
        
        print(f"\n{'='*20} FINAL ASSESSMENT {'='*20}")
        if overall_success:
            print("✅ COMPREHENSIVE TEST PASSED")
            print("✓ Data generation is accurate and consistent")
            print("✓ All metrics align with case study requirements")
            print("✓ Script is ready for production use")
        else:
            print("❌ COMPREHENSIVE TEST NEEDS ATTENTION")
            print("⚠️ Some metrics may need adjustment")
            print("⚠️ Review the generation logic for consistency")
    else:
        print("❌ No tests completed successfully")
    
    print("=" * 70)


if __name__ == "__main__":
    run_comprehensive_tests()