#!/usr/bin/env python3
"""
Database Populator Script for FISST Academy Case Study
Supports MySQL and PostgreSQL databases with simulated security metrics data.
"""

import sys
import random
from decimal import Decimal
from faker import Faker
from faker.providers import BaseProvider
import mysql.connector
import psycopg2
from psycopg2.extras import RealDictCursor


class IndianDataProvider(BaseProvider):
    """Custom Faker provider for Indian-specific data"""
    
    indian_first_names = [
        'Aarav', 'Aditi', 'Amit', 'Ananya', 'Arjun', 'Aisha', 'Deepak', 'Divya',
        'Karan', 'Kavya', 'Manish', 'Meera', 'Nikhil', 'Priya', 'Rahul', 'Riya',
        'Rohit', 'Sanya', 'Suresh', 'Tanya', 'Vikram', 'Vaishali', 'Yash', 'Zoya'
    ]
    
    indian_last_names = [
        'Sharma', 'Verma', 'Singh', 'Kumar', 'Gupta', 'Agarwal', 'Patel', 'Shah',
        'Joshi', 'Reddy', 'Nair', 'Iyer', 'Chandra', 'Mishra', 'Tripathi', 'Yadav'
    ]
    
    indian_cities = [
        'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata',
        'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur'
    ]
    
    def indian_name(self):
        return f"{random.choice(self.indian_first_names)} {random.choice(self.indian_last_names)}"
    
    def indian_phone(self):
        return f"+91 {random.randint(70000, 99999)}{random.randint(10000, 99999)}"
    
    def indian_city(self):
        return random.choice(self.indian_cities)


class DatabasePopulator:
    """Main class for database population and management"""
    
    def __init__(self):
        self.fake = Faker()
        self.fake.add_provider(IndianDataProvider)
        self.connection = None
        self.cursor = None
        self.db_type = None
        
    def get_database_config(self):
        """Get database connection details from user"""
        print("=== Database Connection Configuration ===")
        
        # Get database type
        while True:
            db_type = input("Enter database type (mysql/postgresql): ").lower().strip()
            if db_type in ['mysql', 'postgresql']:
                self.db_type = db_type
                break
            print("Please enter 'mysql' or 'postgresql'")
        
        # Get connection details
        host = input("Enter host (default: localhost): ").strip() or "localhost"
        
        if self.db_type == 'mysql':
            default_port = 3306
        else:
            default_port = 5432
            
        port_input = input(f"Enter port (default: {default_port}): ").strip()
        port = int(port_input) if port_input else default_port
        
        database = input("Enter database name: ").strip()
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        return {
            'host': host,
            'port': port,
            'database': database,
            'username': username,
            'password': password
        }
    
    def connect_to_database(self, config):
        """Establish database connection"""
        try:
            if self.db_type == 'mysql':
                self.connection = mysql.connector.connect(
                    host=config['host'],
                    port=config['port'],
                    database=config['database'],
                    user=config['username'],
                    password=config['password']
                )
                self.cursor = self.connection.cursor(dictionary=True)
            else:  # postgresql
                self.connection = psycopg2.connect(
                    host=config['host'],
                    port=config['port'],
                    database=config['database'],
                    user=config['username'],
                    password=config['password']
                )
                self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            
            print(f"✓ Successfully connected to {self.db_type} database!")
            return True
            
        except Exception as e:
            print(f"✗ Failed to connect to database: {e}")
            return False
    
    def create_tables(self):
        """Create all required tables"""
        tables = {
            'employees': self._get_employees_table_sql(),
            'security_metrics': self._get_security_metrics_table_sql(),
            'usb_incidents': self._get_usb_incidents_table_sql(),
            'intrusion_attempts': self._get_intrusion_attempts_table_sql(),
            'roi_tracking': self._get_roi_tracking_table_sql()
        }
        
        try:
            for table_name, sql in tables.items():
                self.cursor.execute(sql)
                print(f"✓ Created table: {table_name}")
            
            self.connection.commit()
            print("✓ All tables created successfully!")
            
        except Exception as e:
            print(f"✗ Error creating tables: {e}")
            self.connection.rollback()
            return False
        
        return True
    
    def _get_employees_table_sql(self):
        """SQL for employees table"""
        if self.db_type == 'mysql':
            return """
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
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
        else:  # postgresql
            return """
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
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
        """SQL for security metrics table"""
        common_sql = """
        CREATE TABLE IF NOT EXISTS security_metrics (
            id {} PRIMARY KEY,
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
        
        if self.db_type == 'mysql':
            return common_sql.format("INT AUTO_INCREMENT")
        else:
            return common_sql.format("SERIAL")
    
    def _get_usb_incidents_table_sql(self):
        """SQL for USB incidents table"""
        common_sql = """
        CREATE TABLE IF NOT EXISTS usb_incidents (
            id {} PRIMARY KEY,
            employee_id VARCHAR(20) NOT NULL,
            incident_date DATE NOT NULL,
            device_type VARCHAR(50),
            blocked BOOLEAN DEFAULT FALSE,
            location VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
        )
        """
        
        if self.db_type == 'mysql':
            return common_sql.format("INT AUTO_INCREMENT")
        else:
            return common_sql.format("SERIAL")
    
    def _get_intrusion_attempts_table_sql(self):
        """SQL for intrusion attempts table"""
        common_sql = """
        CREATE TABLE IF NOT EXISTS intrusion_attempts (
            id {} PRIMARY KEY,
            attempt_date DATE NOT NULL,
            source_ip VARCHAR(45),
            attempt_type VARCHAR(50),
            blocked_at_reception BOOLEAN DEFAULT TRUE,
            severity VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        if self.db_type == 'mysql':
            return common_sql.format("INT AUTO_INCREMENT")
        else:
            return common_sql.format("SERIAL")
    
    def _get_roi_tracking_table_sql(self):
        """SQL for ROI tracking table"""
        if self.db_type == 'mysql':
            return """
            CREATE TABLE IF NOT EXISTS roi_tracking (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tracking_date DATE NOT NULL,
                engagement_cost DECIMAL(15,2),
                avoided_fraud_amount DECIMAL(15,2),
                roi_multiple DECIMAL(10,2),
                currency VARCHAR(10) DEFAULT 'INR',
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        else:  # postgresql
            return """
            CREATE TABLE IF NOT EXISTS roi_tracking (
                id SERIAL PRIMARY KEY,
                tracking_date DATE NOT NULL,
                engagement_cost DECIMAL(15,2),
                avoided_fraud_amount DECIMAL(15,2),
                roi_multiple DECIMAL(10,2),
                currency VARCHAR(10) DEFAULT 'INR',
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
    
    def check_data_exists(self):
        """Check if data exists in any of the tables"""
        tables = ['employees', 'security_metrics', 'usb_incidents', 'intrusion_attempts', 'roi_tracking']
        
        try:
            for table in tables:
                self.cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                result = self.cursor.fetchone()
                count = result['count'] if isinstance(result, dict) else result[0]
                if count > 0:
                    return True
            return False
        except Exception as e:
            print(f"Error checking data existence: {e}")
            return False
    
    def delete_all_data(self):
        """Delete all data from tables"""
        tables = ['roi_tracking', 'intrusion_attempts', 'usb_incidents', 'security_metrics', 'employees']
        
        try:
            for table in tables:
                self.cursor.execute(f"DELETE FROM {table}")
            self.connection.commit()
            print("✓ All existing data deleted successfully!")
            return True
        except Exception as e:
            print(f"✗ Error deleting data: {e}")
            self.connection.rollback()
            return False
    
    def generate_employees(self, num_employees):
        """Generate employee data"""
        departments = ['IT Security', 'Human Resources', 'Finance', 'Operations', 'Marketing', 'Sales']
        positions = ['Analyst', 'Manager', 'Coordinator', 'Specialist', 'Executive', 'Director']
        
        employees_data = []
        for i in range(num_employees):
            employee_id = f"FISST{str(i+1).zfill(4)}"
            name = self.fake.indian_name()
            email = f"{name.lower().replace(' ', '.')}@fisst.edu"
            phone = self.fake.indian_phone()
            department = random.choice(departments)
            position = random.choice(positions)
            city = self.fake.indian_city()
            address = f"{random.randint(1, 999)}, {self.fake.street_name()}, {city}"
            hire_date = self.fake.date_between(start_date='-5y', end_date='today')
            
            employees_data.append((
                employee_id, name, email, phone, department, position,
                city, address, hire_date
            ))
        
        try:
            sql = """
            INSERT INTO employees (employee_id, name, email, phone, department, position, city, address, hire_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        """Generate security metrics data based on case study"""
        metrics_data = []
        
        # Generate baseline data (22% click rate, 0% reporting)
        baseline_entries = len(employee_ids) * 3  # 3 baseline measurements per employee
        for _ in range(baseline_entries):
            employee_id = random.choice(employee_ids)
            click_rate = random.uniform(20, 24)  # Around 22%
            reporting_rate = 0  # Zero reporting initially
            
            metrics_data.append((
                employee_id,
                self.fake.date_between(start_date='-6m', end_date='-3m'),
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
                self.fake.date_between(start_date='-3m', end_date='today'),
                click_rate,
                reporting_rate,
                random.choice([True, False]),  # training_completed
                random.choice(['Simulation', 'Intrusion Test', 'Training']),
                True   # intervention_applied
            ))
        
        try:
            sql = """
            INSERT INTO security_metrics (employee_id, metric_date, click_rate, reporting_rate, training_completed, simulation_type, intervention_applied)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
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
        """Generate USB incident data"""
        incidents_data = []
        device_types = ['USB Drive', 'External HDD', 'Phone', 'Tablet', 'Unknown Device']
        locations = ['Workstation', 'Conference Room', 'Lab', 'Reception', 'Server Room']
        
        # Generate 11 initial incidents (before intervention)
        for _ in range(11):
            employee_id = random.choice(employee_ids)
            incidents_data.append((
                employee_id,
                self.fake.date_between(start_date='-6m', end_date='-3m'),
                random.choice(device_types),
                False,  # not blocked initially
                random.choice(locations)
            ))
        
        # After intervention: 0 incidents (all blocked)
        # No additional incidents as they're all blocked now
        
        try:
            sql = """
            INSERT INTO usb_incidents (employee_id, incident_date, device_type, blocked, location)
            VALUES (%s, %s, %s, %s, %s)
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
        """Generate intrusion attempts data"""
        attempts_data = []
        attempt_types = ['Phishing', 'Malware', 'Social Engineering', 'Network Scan', 'Brute Force']
        severities = ['Low', 'Medium', 'High', 'Critical']
        
        # Generate various intrusion attempts, all blocked at reception
        for _ in range(50):
            attempts_data.append((
                self.fake.date_between(start_date='-6m', end_date='today'),
                self.fake.ipv4(),
                random.choice(attempt_types),
                True,  # blocked_at_reception
                random.choice(severities)
            ))
        
        try:
            sql = """
            INSERT INTO intrusion_attempts (attempt_date, source_ip, attempt_type, blocked_at_reception, severity)
            VALUES (%s, %s, %s, %s, %s)
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
        """Generate ROI tracking data"""
        # Based on case study: ₹7.3 crore avoided, 15x+ ROI
        engagement_cost = Decimal('48666666.67')  # ₹7.3 crore / 15 = approx ₹48.67 lakh
        avoided_fraud = Decimal('730000000.00')  # ₹7.3 crore
        roi_multiple = Decimal('15.0')
        
        roi_data = [(
            self.fake.date_between(start_date='-1m', end_date='today'),
            engagement_cost,
            avoided_fraud,
            roi_multiple,
            'INR',
            'Avoided phishing payroll fraud through security awareness training and intervention measures'
        )]
        
        try:
            sql = """
            INSERT INTO roi_tracking (tracking_date, engagement_cost, avoided_fraud_amount, roi_multiple, currency, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.executemany(sql, roi_data)
            self.connection.commit()
            print(f"✓ Generated ROI tracking entry!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating ROI tracking: {e}")
            self.connection.rollback()
            return False
    
    def display_existing_data(self):
        """Display summary of existing data"""
        print("\n=== Existing Data Summary ===")
        
        tables = {
            'employees': 'SELECT COUNT(*) as count FROM employees',
            'security_metrics': 'SELECT COUNT(*) as count FROM security_metrics',
            'usb_incidents': 'SELECT COUNT(*) as count FROM usb_incidents',
            'intrusion_attempts': 'SELECT COUNT(*) as count FROM intrusion_attempts',
            'roi_tracking': 'SELECT COUNT(*) as count FROM roi_tracking'
        }
        
        for table_name, query in tables.items():
            try:
                self.cursor.execute(query)
                result = self.cursor.fetchone()
                count = result['count'] if isinstance(result, dict) else result[0]
                print(f"{table_name.replace('_', ' ').title()}: {count} records")
            except Exception as e:
                print(f"Error querying {table_name}: {e}")
    
    def display_statistics_summary(self):
        """Display statistics summary after data generation"""
        print("\n=== Generated Data Statistics Summary ===")
        
        try:
            # Security metrics summary
            self.cursor.execute("""
                SELECT 
                    AVG(CASE WHEN intervention_applied = FALSE THEN click_rate END) as baseline_click_rate,
                    AVG(CASE WHEN intervention_applied = TRUE THEN click_rate END) as post_intervention_click_rate,
                    AVG(CASE WHEN intervention_applied = FALSE THEN reporting_rate END) as baseline_reporting_rate,
                    AVG(CASE WHEN intervention_applied = TRUE THEN reporting_rate END) as post_intervention_reporting_rate
                FROM security_metrics
            """)
            
            metrics = self.cursor.fetchone()
            if metrics:
                baseline_click = metrics['baseline_click_rate'] if isinstance(metrics, dict) else metrics[0]
                post_click = metrics['post_intervention_click_rate'] if isinstance(metrics, dict) else metrics[1]
                baseline_report = metrics['baseline_reporting_rate'] if isinstance(metrics, dict) else metrics[2]
                post_report = metrics['post_intervention_reporting_rate'] if isinstance(metrics, dict) else metrics[3]
                
                print(f"Click Rate: {baseline_click:.1f}% (baseline) → {post_click:.1f}% (post-intervention)")
                print(f"Reporting Rate: {baseline_report:.1f}% (baseline) → {post_report:.1f}% (post-intervention)")
            
            # USB incidents
            self.cursor.execute("SELECT COUNT(*) as count FROM usb_incidents WHERE blocked = FALSE")
            result = self.cursor.fetchone()
            usb_incidents = result['count'] if isinstance(result, dict) else result[0]
            print(f"USB Incidents: {usb_incidents} (before intervention) → 0 (after intervention)")
            
            # Intrusion attempts
            self.cursor.execute("SELECT COUNT(*) as count FROM intrusion_attempts WHERE blocked_at_reception = TRUE")
            result = self.cursor.fetchone()
            blocked_intrusions = result['count'] if isinstance(result, dict) else result[0]
            print(f"Intrusion Attempts: {blocked_intrusions} blocked at reception")
            
            # ROI
            self.cursor.execute("SELECT avoided_fraud_amount, roi_multiple FROM roi_tracking LIMIT 1")
            result = self.cursor.fetchone()
            if result:
                avoided_fraud = result['avoided_fraud_amount'] if isinstance(result, dict) else result[0]
                roi_multiple = result['roi_multiple'] if isinstance(result, dict) else result[1]
                print(f"ROI: ₹{float(avoided_fraud)/10000000:.1f} crore avoided fraud, {float(roi_multiple):.0f}x return on investment")
            
        except Exception as e:
            print(f"Error generating statistics: {e}")
    
    def get_employee_ids(self):
        """Get list of employee IDs"""
        try:
            self.cursor.execute("SELECT employee_id FROM employees")
            results = self.cursor.fetchall()
            return [row['employee_id'] if isinstance(row, dict) else row[0] for row in results]
        except Exception as e:
            print(f"Error fetching employee IDs: {e}")
            return []
    
    def close_connection(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("✓ Database connection closed")


def get_yes_no_input(prompt):
    """Get yes/no input from user"""
    while True:
        response = input(f"{prompt} (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'")


def main():
    """Main function"""
    print("FISST Academy Database Populator")
    print("=" * 40)
    
    populator = DatabasePopulator()
    
    try:
        # Get database configuration
        config = populator.get_database_config()
        
        # Connect to database
        if not populator.connect_to_database(config):
            return
        
        # Create tables
        if not populator.create_tables():
            return
        
        # Check if data exists
        data_exists = populator.check_data_exists()
        
        if data_exists:
            print("\n⚠️  Data already exists in the database tables.")
            populator.display_existing_data()
            
            delete_data = get_yes_no_input("\nDo you want to delete all existing data?")
            
            if delete_data:
                if not populator.delete_all_data():
                    return
                
                generate_new = get_yes_no_input("Do you want to generate fresh data?")
                if not generate_new:
                    print("Data deleted. Exiting...")
                    return
            else:
                print("Keeping existing data. Exiting...")
                return
        
        # Generate data flow
        if not data_exists or delete_data:
            while True:
                try:
                    num_employees = int(input("\nEnter the number of employees to create: "))
                    if num_employees > 0:
                        break
                    else:
                        print("Please enter a positive number")
                except ValueError:
                    print("Please enter a valid number")
            
            print(f"\nGenerating data for {num_employees} employees...")
            
            # Generate all data
            if populator.generate_employees(num_employees):
                employee_ids = populator.get_employee_ids()
                
                if (populator.generate_security_metrics(employee_ids) and
                    populator.generate_usb_incidents(employee_ids) and
                    populator.generate_intrusion_attempts() and
                    populator.generate_roi_tracking()):
                    
                    print("\n✓ All data generated successfully!")
                    populator.display_statistics_summary()
                else:
                    print("\n✗ Some data generation failed")
            else:
                print("\n✗ Employee generation failed")
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
    finally:
        populator.close_connection()


if __name__ == "__main__":
    main()