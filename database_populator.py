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
        """Create all required tables based on the provided ER diagram"""
        tables = {
            'employee_master': self._get_employee_master_table_sql(),
            'employee_phish_smish_sim': self._get_employee_phish_smish_sim_table_sql(),
            'employee_vishing_sim': self._get_employee_vishing_sim_table_sql(),
            'employee_quishing_sim': self._get_employee_quishing_sim_table_sql(),
            'red_team_assessment': self._get_red_team_assessment_table_sql()
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
    
    def _get_employee_master_table_sql(self):
        """SQL for employee_master table based on ER diagram"""
        if self.db_type == 'mysql':
            return """
            CREATE TABLE IF NOT EXISTS employee_master (
                serial_no INT AUTO_INCREMENT PRIMARY KEY,
                employee_id VARCHAR(20) UNIQUE NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                gender CHAR(1),
                date_of_birth DATE,
                age INT,
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
                total_employees_at_branch INT,
                security_level VARCHAR(20),
                building_storeys INT,
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
        else:  # postgresql
            return """
            CREATE TABLE IF NOT EXISTS employee_master (
                serial_no SERIAL PRIMARY KEY,
                employee_id VARCHAR(20) UNIQUE NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                gender CHAR(1),
                date_of_birth DATE,
                age INT,
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
                total_employees_at_branch INT,
                security_level VARCHAR(20),
                building_storeys INT,
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
        """SQL for employee_phish_smish_sim table"""
        common_sql = """
        CREATE TABLE IF NOT EXISTS employee_phish_smish_sim (
            sim_id {} PRIMARY KEY,
            employee_id VARCHAR(20) NOT NULL,
            simulation_type VARCHAR(50),
            work_email VARCHAR(100),
            personal_email VARCHAR(100),
            click_response_rate DECIMAL(5,2),
            testing_status VARCHAR(20),
            FOREIGN KEY (employee_id) REFERENCES employee_master(employee_id) ON DELETE CASCADE
        )
        """
        
        if self.db_type == 'mysql':
            return common_sql.format("INT AUTO_INCREMENT")
        else:
            return common_sql.format("SERIAL")
    
    def _get_employee_vishing_sim_table_sql(self):
        """SQL for employee_vishing_sim table"""
        common_sql = """
        CREATE TABLE IF NOT EXISTS employee_vishing_sim (
            sim_id {} PRIMARY KEY,
            employee_id VARCHAR(20) NOT NULL,
            phone_number VARCHAR(20),
            alt_phone_number VARCHAR(20),
            vish_response_rate DECIMAL(5,2),
            testing_status VARCHAR(20),
            FOREIGN KEY (employee_id) REFERENCES employee_master(employee_id) ON DELETE CASCADE
        )
        """
        
        if self.db_type == 'mysql':
            return common_sql.format("INT AUTO_INCREMENT")
        else:
            return common_sql.format("SERIAL")
    
    def _get_employee_quishing_sim_table_sql(self):
        """SQL for employee_quishing_sim table (QR code phishing)"""
        common_sql = """
        CREATE TABLE IF NOT EXISTS employee_quishing_sim (
            sim_id {} PRIMARY KEY,
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
        
        if self.db_type == 'mysql':
            return common_sql.format("INT AUTO_INCREMENT")
        else:
            return common_sql.format("SERIAL")
    
    def _get_red_team_assessment_table_sql(self):
        """SQL for red_team_assessment table"""
        common_sql = """
        CREATE TABLE IF NOT EXISTS red_team_assessment (
            assess_id {} PRIMARY KEY,
            employee_id VARCHAR(20) NOT NULL,
            branch_code VARCHAR(10),
            local_employees_at_branch INT,
            security_level VARCHAR(20),
            building_storeys INT,
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
        
        if self.db_type == 'mysql':
            return common_sql.format("INT AUTO_INCREMENT")
        else:
            return common_sql.format("SERIAL")
    
    def check_data_exists(self):
        """Check if data exists in any of the tables"""
        tables = ['employee_master', 'employee_phish_smish_sim', 'employee_vishing_sim', 'employee_quishing_sim', 'red_team_assessment']
        
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
        """Delete all data from tables in correct order (respecting foreign keys)"""
        tables = ['red_team_assessment', 'employee_quishing_sim', 'employee_vishing_sim', 'employee_phish_smish_sim', 'employee_master']
        
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
        """Generate employee master data based on ER diagram"""
        departments = ['IT Security', 'Human Resources', 'Finance', 'Operations', 'Marketing', 'Sales', 'Research', 'Admin']
        designations = ['Analyst', 'Manager', 'Coordinator', 'Specialist', 'Executive', 'Director', 'Team Lead', 'Senior Analyst']
        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        marital_statuses = ['Single', 'Married', 'Divorced', 'Widowed']
        indian_states = ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Delhi', 'Uttar Pradesh', 'Gujarat', 'West Bengal', 'Rajasthan']
        branch_codes = ['MUM01', 'DEL02', 'BLR03', 'HYD04', 'CHN05', 'KOL06', 'PUN07', 'AHM08']
        branch_locations = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']
        
        employees_data = []
        used_emails = set()
        
        for i in range(num_employees):
            employee_id = f"FISST{str(i+1).zfill(4)}"
            
            # Generate Indian name components
            name_parts = self.fake.indian_name().split()
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else 'Kumar'
            
            # Generate unique emails
            base_work_email = f"{first_name.lower()}.{last_name.lower()}"
            work_email = f"{base_work_email}@fisst.edu"
            counter = 1
            while work_email in used_emails:
                work_email = f"{base_work_email}{counter}@fisst.edu"
                counter += 1
            used_emails.add(work_email)
            
            personal_email = f"{base_work_email}@gmail.com"
            email = work_email  # Primary email
            
            # Generate other details
            gender = random.choice(['M', 'F'])
            date_of_birth = self.fake.date_between(start_date='-65y', end_date='-22y')
            age = 2024 - date_of_birth.year
            blood_group = random.choice(blood_groups)
            marital_status = random.choice(marital_statuses)
            phone_number = self.fake.indian_phone()
            city = self.fake.indian_city()
            address = f"{random.randint(1, 999)}, {self.fake.street_name()}, {city}"
            state = random.choice(indian_states)
            postal_code = str(random.randint(100000, 999999))
            country = 'India'
            designation = random.choice(designations)
            department = random.choice(departments)
            salary = random.uniform(300000, 2000000)  # INR salary range
            work_experience_years = random.uniform(0.5, 20.0)
            joining_date = self.fake.date_between(start_date='-10y', end_date='today')
            
            # Emergency contact
            emergency_contact_name = self.fake.indian_name()
            emergency_contact_phone = self.fake.indian_phone()
            
            # Family and medical details
            family_details = f"Family of {random.randint(2, 6)} members"
            medical_conditions = random.choice(['None', 'Diabetes', 'Hypertension', 'Asthma', 'None', 'None'])  # Most have None
            
            # Simulation data - baseline values
            simulation_type = 'Baseline Assessment'
            click_response_rate = random.uniform(21, 25)  # Updated: 21-25% for phishing baseline
            phish_test_simulation_date = self.fake.date_between(start_date='-6m', end_date='-3m')
            phish_testing_status = 'Completed'
            
            # Vishing data
            vishing_phone_number = phone_number
            vishing_alt_phone_number = self.fake.indian_phone()
            voice_auth_test = random.choice([True, False])
            vish_response_rate = random.uniform(23, 28)  # Updated: 23-28% for vishing baseline
            vish_test_simulation_date = self.fake.date_between(start_date='-6m', end_date='-3m')
            vish_testing_status = 'Completed'
            
            # Branch and assessment data
            branch_idx = i % len(branch_codes)
            branch_location = branch_locations[branch_idx]
            branch_code = branch_codes[branch_idx]
            total_employees_at_branch = random.randint(15, 50)
            security_level = random.choice(['Low', 'Medium', 'High'])
            building_storeys = random.randint(1, 10)
            
            # Assessment details
            assessment_date = self.fake.date_between(start_date='-3m', end_date='today')
            assessment_time_start = self.fake.time()
            assessment_time_end = self.fake.time()
            permission_granted = random.choice([True, False])
            approving_official_name = self.fake.indian_name()
            approving_official_designation = random.choice(['Manager', 'Director', 'VP', 'Senior Manager'])
            
            # Security flags
            identity_verification_required = True
            identity_verified = random.choice([True, False])
            security_guard_present = random.choice([True, False])
            visitor_log_maintained = True
            badge_issued = random.choice([True, False])
            escort_required = random.choice([True, False])
            restricted_areas_accessed = random.choice([True, False])
            tailgating_possible = random.choice([True, False])
            social_engineering_successful = random.choice([True, False])
            
            # Scores (post-intervention should be higher)
            physical_security_score = random.uniform(6.0, 9.0)
            human_security_score = random.uniform(7.0, 9.5)
            overall_assessment_score = (physical_security_score + human_security_score) / 2
            
            # Assessment details
            vulnerabilities_found = random.choice([
                'Weak access controls', 'Inadequate visitor management', 'Social engineering susceptibility',
                'Poor password practices', 'Unsecured workstations', 'None significant'
            ])
            recommendations = random.choice([
                'Implement two-factor authentication', 'Enhanced security training',
                'Improve visitor access controls', 'Regular security assessments',
                'Employee awareness programs', 'Continue current practices'
            ])
            assessor_name = self.fake.indian_name()
            assessor_id = f"ASST{random.randint(1, 20):02d}"
            notes = f"Assessment completed for {department} department employee"
            red_team_testing_status = 'Completed'
            
            employees_data.append((
                employee_id, first_name, last_name, gender, date_of_birth, age, blood_group, marital_status,
                email, phone_number, address, state, postal_code, country, designation, department,
                salary, work_experience_years, joining_date, emergency_contact_name, emergency_contact_phone,
                family_details, medical_conditions, simulation_type, work_email, personal_email,
                click_response_rate, phish_test_simulation_date, phish_testing_status,
                vishing_phone_number, vishing_alt_phone_number, voice_auth_test, vish_response_rate,
                vish_test_simulation_date, vish_testing_status, branch_location, branch_code,
                total_employees_at_branch, security_level, building_storeys, assessment_date,
                assessment_time_start, assessment_time_end, permission_granted, approving_official_name,
                approving_official_designation, identity_verification_required, identity_verified,
                security_guard_present, visitor_log_maintained, badge_issued, escort_required,
                restricted_areas_accessed, tailgating_possible, social_engineering_successful,
                physical_security_score, human_security_score, overall_assessment_score,
                vulnerabilities_found, recommendations, assessor_name, assessor_id, notes, red_team_testing_status
            ))
        
        try:
            sql = """
            INSERT INTO employee_master (
                employee_id, first_name, last_name, gender, date_of_birth, age, blood_group, marital_status,
                email, phone_number, address, state, postal_code, country, designation, department,
                salary, work_experience_years, joining_date, emergency_contact_name, emergency_contact_phone,
                family_details, medical_conditions, simulation_type, work_email, personal_email,
                click_response_rate, phish_test_simulation_date, phish_testing_status,
                vishing_phone_number, vishing_alt_phone_number, voice_auth_test, vish_response_rate,
                vish_test_simulation_date, vish_testing_status, branch_location, branch_code,
                total_employees_at_branch, security_level, building_storeys, assessment_date,
                assessment_time_start, assessment_time_end, permission_granted, approving_official_name,
                approving_official_designation, identity_verification_required, identity_verified,
                security_guard_present, visitor_log_maintained, badge_issued, escort_required,
                restricted_areas_accessed, tailgating_possible, social_engineering_successful,
                physical_security_score, human_security_score, overall_assessment_score,
                vulnerabilities_found, recommendations, assessor_name, assessor_id, notes, red_team_testing_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.executemany(sql, employees_data)
            self.connection.commit()
            print(f"✓ Generated {num_employees} employees in employee_master table!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating employees: {e}")
            self.connection.rollback()
            return False
    
    def generate_phish_smish_simulations(self, employee_ids):
        """Generate phishing/smishing simulation data"""
        sim_data = []
        simulation_types = ['Email Phishing', 'SMS Phishing', 'Social Media Phishing']
        testing_statuses = ['Completed', 'Pending', 'Failed', 'Passed']
        
        for employee_id in employee_ids:
            # Generate multiple simulation entries per employee
            for _ in range(random.randint(2, 4)):
                # Get employee work and personal email from employee_master
                work_email = f"{employee_id.lower().replace('fisst', 'emp')}@fisst.edu"
                personal_email = f"{employee_id.lower().replace('fisst', 'emp')}@gmail.com"
                
                # Updated failure rates: 21-25% for phishing/smishing simulations
                click_response_rate = random.uniform(21, 25)
                
                sim_data.append((
                    employee_id,
                    random.choice(simulation_types),
                    work_email,
                    personal_email,
                    click_response_rate,
                    random.choice(testing_statuses)
                ))
        
        try:
            sql = """
            INSERT INTO employee_phish_smish_sim (employee_id, simulation_type, work_email, personal_email, click_response_rate, testing_status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.executemany(sql, sim_data)
            self.connection.commit()
            print(f"✓ Generated {len(sim_data)} phishing/smishing simulation entries!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating phish/smish simulations: {e}")
            self.connection.rollback()
            return False
    
    def generate_vishing_simulations(self, employee_ids):
        """Generate vishing (voice phishing) simulation data"""
        sim_data = []
        testing_statuses = ['Completed', 'Pending', 'Failed', 'Passed']
        
        for employee_id in employee_ids:
            # Generate vishing simulation entries
            for _ in range(random.randint(1, 3)):
                phone_number = self.fake.indian_phone()
                alt_phone_number = self.fake.indian_phone()
                
                # Updated failure rates: 26-30% for vishing simulations  
                vish_response_rate = random.uniform(26, 30)
                
                sim_data.append((
                    employee_id,
                    phone_number,
                    alt_phone_number,
                    vish_response_rate,
                    random.choice(testing_statuses)
                ))
        
        try:
            sql = """
            INSERT INTO employee_vishing_sim (employee_id, phone_number, alt_phone_number, vish_response_rate, testing_status)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            self.cursor.executemany(sql, sim_data)
            self.connection.commit()
            print(f"✓ Generated {len(sim_data)} vishing simulation entries!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating vishing simulations: {e}")
            self.connection.rollback()
            return False
    
    def generate_quishing_simulations(self, employee_ids):
        """Generate quishing (QR code phishing) simulation data"""
        sim_data = []
        qr_code_types = ['Payment QR', 'WiFi QR', 'App Download QR', 'Survey QR', 'Menu QR', 'Contact QR']
        device_types = ['Mobile Phone', 'Tablet', 'Laptop', 'Desktop']
        testing_statuses = ['Completed', 'Pending', 'Failed', 'Passed']
        
        for employee_id in employee_ids:
            # Generate quishing simulation entries
            for _ in range(random.randint(1, 2)):
                qr_code_type = random.choice(qr_code_types)
                
                # Updated failure rates: 22-27% for quishing (QR code) simulations
                qr_scan_rate = random.uniform(22, 27)
                malicious_qr_clicked = random.choice([True, False])
                device_type = random.choice(device_types)
                testing_status = random.choice(testing_statuses)
                simulation_date = self.fake.date_between(start_date='-6m', end_date='today')
                
                sim_data.append((
                    employee_id,
                    qr_code_type,
                    qr_scan_rate,
                    malicious_qr_clicked,
                    device_type,
                    testing_status,
                    simulation_date
                ))
        
        try:
            sql = """
            INSERT INTO employee_quishing_sim (employee_id, qr_code_type, qr_scan_rate, malicious_qr_clicked, device_type, testing_status, simulation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.executemany(sql, sim_data)
            self.connection.commit()
            print(f"✓ Generated {len(sim_data)} quishing simulation entries!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating quishing simulations: {e}")
            self.connection.rollback()
            return False
    
    def generate_red_team_assessments(self, employee_ids):
        """Generate red team assessment data"""
        assessment_data = []
        security_levels = ['Low', 'Medium', 'High', 'Critical']
        testing_statuses = ['Completed', 'In Progress', 'Scheduled', 'Cancelled']
        branch_codes = ['MUM01', 'DEL02', 'BLR03', 'HYD04', 'CHN05', 'KOL06', 'PUN07', 'AHM08']
        
        for employee_id in employee_ids:
            # Generate assessment entries (not every employee gets assessed)
            if random.random() < 0.7:  # 70% of employees get assessed
                branch_code = random.choice(branch_codes)
                local_employees_at_branch = random.randint(15, 50)
                security_level = random.choice(security_levels)
                building_storeys = random.randint(1, 10)
                assessment_date = self.fake.date_between(start_date='-3m', end_date='today')
                assessment_time_start = self.fake.time()
                assessment_time_end = self.fake.time()
                permission_granted = random.choice([True, False])
                approving_official_name = self.fake.indian_name()
                approving_official_designation = random.choice(['Manager', 'Director', 'VP', 'Senior Manager'])
                
                # Security measures
                identity_verification_required = True
                identity_verified = random.choice([True, False])
                security_guard_present = random.choice([True, False])
                visitor_log_maintained = True
                badge_issued = random.choice([True, False])
                escort_required = random.choice([True, False])
                restricted_areas_accessed = random.choice([True, False])
                tailgating_possible = random.choice([True, False])
                social_engineering_successful = random.choice([True, False])
                
                # Assessment scores (higher scores = better security)
                physical_security_score = random.uniform(6.0, 9.5)
                human_security_score = random.uniform(7.0, 9.0)
                overall_assessment_score = (physical_security_score + human_security_score) / 2
                
                vulnerabilities_found = random.choice([
                    'Weak access controls, tailgating possible',
                    'Social engineering susceptibility',
                    'Inadequate visitor management',
                    'Poor workstation security',
                    'None significant',
                    'Badge verification issues'
                ])
                
                recommendations = random.choice([
                    'Implement stricter access controls',
                    'Enhanced security awareness training',
                    'Improve visitor management system',
                    'Regular security audits',
                    'Deploy additional security measures',
                    'Continue monitoring'
                ])
                
                assessor_name = self.fake.indian_name()
                assessor_id = f"ASST{random.randint(1, 20):02d}"
                notes = f"Red team assessment completed - {security_level} security level facility"
                testing_status = random.choice(testing_statuses)
                
                assessment_data.append((
                    employee_id, branch_code, local_employees_at_branch, security_level, building_storeys,
                    assessment_date, assessment_time_start, assessment_time_end, permission_granted,
                    approving_official_name, approving_official_designation, identity_verification_required,
                    identity_verified, security_guard_present, visitor_log_maintained, badge_issued,
                    escort_required, restricted_areas_accessed, tailgating_possible, social_engineering_successful,
                    physical_security_score, human_security_score, overall_assessment_score,
                    vulnerabilities_found, recommendations, assessor_name, assessor_id, notes, testing_status
                ))
        
        try:
            sql = """
            INSERT INTO red_team_assessment (
                employee_id, branch_code, local_employees_at_branch, security_level, building_storeys,
                assessment_date, assessment_time_start, assessment_time_end, permission_granted,
                approving_official_name, approving_official_designation, identity_verification_required,
                identity_verified, security_guard_present, visitor_log_maintained, badge_issued,
                escort_required, restricted_areas_accessed, tailgating_possible, social_engineering_successful,
                physical_security_score, human_security_score, overall_assessment_score,
                vulnerabilities_found, recommendations, assessor_name, assessor_id, notes, testing_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.executemany(sql, assessment_data)
            self.connection.commit()
            print(f"✓ Generated {len(assessment_data)} red team assessment entries!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating red team assessments: {e}")
            self.connection.rollback()
            return False
    
    def display_existing_data(self):
        """Display summary of existing data"""
        print("\n=== Existing Data Summary ===")
        
        tables = {
            'employee_master': 'SELECT COUNT(*) as count FROM employee_master',
            'employee_phish_smish_sim': 'SELECT COUNT(*) as count FROM employee_phish_smish_sim',
            'employee_vishing_sim': 'SELECT COUNT(*) as count FROM employee_vishing_sim',
            'employee_quishing_sim': 'SELECT COUNT(*) as count FROM employee_quishing_sim',
            'red_team_assessment': 'SELECT COUNT(*) as count FROM red_team_assessment'
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
            # Employee master summary
            self.cursor.execute("SELECT COUNT(*) as count FROM employee_master")
            result = self.cursor.fetchone()
            total_employees = result['count'] if isinstance(result, dict) else result[0]
            print(f"Total Employees: {total_employees}")
            
            # Phishing simulation summary
            self.cursor.execute("""
                SELECT 
                    AVG(click_response_rate) as avg_click_rate,
                    MIN(click_response_rate) as min_click_rate,
                    MAX(click_response_rate) as max_click_rate,
                    COUNT(*) as total_sims
                FROM employee_phish_smish_sim
            """)
            
            phish_metrics = self.cursor.fetchone()
            if phish_metrics:
                avg_click = phish_metrics['avg_click_rate'] if isinstance(phish_metrics, dict) else phish_metrics[0]
                min_click = phish_metrics['min_click_rate'] if isinstance(phish_metrics, dict) else phish_metrics[1]
                max_click = phish_metrics['max_click_rate'] if isinstance(phish_metrics, dict) else phish_metrics[2]
                total_sims = phish_metrics['total_sims'] if isinstance(phish_metrics, dict) else phish_metrics[3]
                
                print(f"Phishing Simulations: {total_sims} total")
                print(f"Click Response Rate: {avg_click:.1f}% (avg), {min_click:.1f}%-{max_click:.1f}% (range)")
            
            # Vishing simulation summary
            self.cursor.execute("""
                SELECT 
                    AVG(vish_response_rate) as avg_vish_rate,
                    COUNT(*) as total_vish_sims
                FROM employee_vishing_sim
            """)
            
            vish_metrics = self.cursor.fetchone()
            if vish_metrics:
                avg_vish = vish_metrics['avg_vish_rate'] if isinstance(vish_metrics, dict) else vish_metrics[0]
                total_vish = vish_metrics['total_vish_sims'] if isinstance(vish_metrics, dict) else vish_metrics[1]
                print(f"Vishing Simulations: {total_vish} total")
                print(f"Vishing Response Rate: {avg_vish:.1f}% (avg)")
            
            # Quishing simulation summary
            self.cursor.execute("""
                SELECT 
                    AVG(qr_scan_rate) as avg_qr_scan_rate,
                    COUNT(*) as total_quishing_sims,
                    SUM(CASE WHEN malicious_qr_clicked = TRUE THEN 1 ELSE 0 END) as malicious_clicks
                FROM employee_quishing_sim
            """)
            
            quish_metrics = self.cursor.fetchone()
            if quish_metrics:
                avg_qr_scan = quish_metrics['avg_qr_scan_rate'] if isinstance(quish_metrics, dict) else quish_metrics[0]
                total_quish = quish_metrics['total_quishing_sims'] if isinstance(quish_metrics, dict) else quish_metrics[1]
                malicious_clicks = quish_metrics['malicious_clicks'] if isinstance(quish_metrics, dict) else quish_metrics[2]
                print(f"Quishing Simulations: {total_quish} total")
                print(f"QR Scan Rate: {avg_qr_scan:.1f}% (avg), Malicious Clicks: {malicious_clicks}")
            
            # Red team assessment summary
            self.cursor.execute("""
                SELECT 
                    AVG(physical_security_score) as avg_physical_score,
                    AVG(human_security_score) as avg_human_score,
                    AVG(overall_assessment_score) as avg_overall_score,
                    COUNT(*) as total_assessments
                FROM red_team_assessment
            """)
            
            assessment_metrics = self.cursor.fetchone()
            if assessment_metrics:
                avg_physical = assessment_metrics['avg_physical_score'] if isinstance(assessment_metrics, dict) else assessment_metrics[0]
                avg_human = assessment_metrics['avg_human_score'] if isinstance(assessment_metrics, dict) else assessment_metrics[1]
                avg_overall = assessment_metrics['avg_overall_score'] if isinstance(assessment_metrics, dict) else assessment_metrics[2]
                total_assessments = assessment_metrics['total_assessments'] if isinstance(assessment_metrics, dict) else assessment_metrics[3]
                
                print(f"Red Team Assessments: {total_assessments} completed")
                print(f"Security Scores - Physical: {avg_physical:.1f}, Human: {avg_human:.1f}, Overall: {avg_overall:.1f}")
            
            # Branch distribution
            self.cursor.execute("""
                SELECT branch_code, branch_location, COUNT(*) as employee_count
                FROM employee_master 
                GROUP BY branch_code, branch_location
                ORDER BY employee_count DESC
            """)
            
            branch_results = self.cursor.fetchall()
            if branch_results:
                print(f"\nBranch Distribution:")
                for row in branch_results:
                    if isinstance(row, dict):
                        print(f"  {row['branch_code']} ({row['branch_location']}): {row['employee_count']} employees")
                    else:
                        print(f"  {row[0]} ({row[1]}): {row[2]} employees")
            
        except Exception as e:
            print(f"Error generating statistics: {e}")
    
    def get_employee_ids(self):
        """Get list of employee IDs"""
        try:
            self.cursor.execute("SELECT employee_id FROM employee_master")
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
                
                if (populator.generate_phish_smish_simulations(employee_ids) and
                    populator.generate_vishing_simulations(employee_ids) and
                    populator.generate_quishing_simulations(employee_ids) and
                    populator.generate_red_team_assessments(employee_ids)):
                    
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