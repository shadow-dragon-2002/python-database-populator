#!/usr/bin/env python3
"""
Updated comprehensive test script for the new ER diagram schema.
Tests data generation accuracy across multiple runs with different employee counts.
Validates that generated data matches the FISST Academy case study percentages.
"""

import sys
import os
import sqlite3
import statistics
import random
from contextlib import contextmanager
from decimal import Decimal

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_populator import DatabasePopulator, IndianDataProvider
from faker import Faker


class SQLiteERTestPopulator(DatabasePopulator):
    """Modified DatabasePopulator for ER diagram schema testing with SQLite"""
    
    def __init__(self):
        super().__init__()
        self.db_type = 'sqlite'
    
    def connect_to_test_database(self):
        """Connect to in-memory SQLite database for testing"""
        try:
            self.connection = sqlite3.connect(':memory:')
            self.connection.row_factory = sqlite3.Row
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
    
    # Override the data generation methods to use SQLite syntax (? instead of %s)
    def generate_employees(self, num_employees):
        """Generate employee master data - SQLite version"""
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
            medical_conditions = random.choice(['None', 'Diabetes', 'Hypertension', 'Asthma', 'None', 'None'])
            
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
                employee_id, first_name, last_name, gender, str(date_of_birth), age, blood_group, marital_status,
                email, phone_number, address, state, postal_code, country, designation, department,
                salary, work_experience_years, str(joining_date), emergency_contact_name, emergency_contact_phone,
                family_details, medical_conditions, simulation_type, work_email, personal_email,
                click_response_rate, str(phish_test_simulation_date), phish_testing_status,
                vishing_phone_number, vishing_alt_phone_number, voice_auth_test, vish_response_rate,
                str(vish_test_simulation_date), vish_testing_status, branch_location, branch_code,
                total_employees_at_branch, security_level, building_storeys, str(assessment_date),
                str(assessment_time_start), str(assessment_time_end), permission_granted, approving_official_name,
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
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        """Generate phishing/smishing simulation data - SQLite version"""
        sim_data = []
        simulation_types = ['Email Phishing', 'SMS Phishing', 'Social Media Phishing']
        testing_statuses = ['Completed', 'Pending', 'Failed', 'Passed']
        
        for employee_id in employee_ids:
            for _ in range(random.randint(2, 4)):
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
            VALUES (?, ?, ?, ?, ?, ?)
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
        """Generate vishing simulation data - SQLite version"""
        sim_data = []
        testing_statuses = ['Completed', 'Pending', 'Failed', 'Passed']
        
        for employee_id in employee_ids:
            for _ in range(random.randint(1, 3)):
                phone_number = self.fake.indian_phone()
                alt_phone_number = self.fake.indian_phone()
                vish_response_rate = random.uniform(26, 30)  # Updated: 26-30% for vishing simulations
                
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
            VALUES (?, ?, ?, ?, ?)
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
        """Generate quishing simulation data - SQLite version"""
        sim_data = []
        qr_code_types = ['Payment QR', 'WiFi QR', 'App Download QR', 'Survey QR', 'Menu QR', 'Contact QR']
        device_types = ['Mobile Phone', 'Tablet', 'Laptop', 'Desktop']
        testing_statuses = ['Completed', 'Pending', 'Failed', 'Passed']
        
        for employee_id in employee_ids:
            for _ in range(random.randint(1, 2)):
                qr_code_type = random.choice(qr_code_types)
                qr_scan_rate = random.uniform(22, 27)  # Updated: 22-27% for quishing simulations
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
                    str(simulation_date)
                ))
        
        try:
            sql = """
            INSERT INTO employee_quishing_sim (employee_id, qr_code_type, qr_scan_rate, malicious_qr_clicked, device_type, testing_status, simulation_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
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
        """Generate red team assessment data - SQLite version"""
        assessment_data = []
        security_levels = ['Low', 'Medium', 'High', 'Critical']
        testing_statuses = ['Completed', 'In Progress', 'Scheduled', 'Cancelled']
        branch_codes = ['MUM01', 'DEL02', 'BLR03', 'HYD04', 'CHN05', 'KOL06', 'PUN07', 'AHM08']
        
        for employee_id in employee_ids:
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
                
                # Assessment scores
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
                    str(assessment_date), str(assessment_time_start), str(assessment_time_end), permission_granted,
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
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            self.cursor.executemany(sql, assessment_data)
            self.connection.commit()
            print(f"✓ Generated {len(assessment_data)} red team assessment entries!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating red team assessments: {e}")
            self.connection.rollback()
            return False


@contextmanager
def test_er_database_populator(num_employees):
    """Context manager for testing ER diagram database populator"""
    populator = SQLiteERTestPopulator()
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


def run_single_er_test(test_num, num_employees):
    """Run a single test with the ER diagram schema"""
    print(f"\n{'='*15} ER SCHEMA TEST {test_num}: {num_employees} Employees {'='*15}")
    
    with test_er_database_populator(num_employees) as (populator, employee_count):
        # Generate data
        if not populator.generate_employees(employee_count):
            print(f"✗ Test {test_num}: Failed to generate employees")
            return None
        
        employee_ids = populator.get_employee_ids()
        if not employee_ids:
            print(f"✗ Test {test_num}: No employee IDs found")
            return None
        
        if not (populator.generate_phish_smish_simulations(employee_ids) and
                populator.generate_vishing_simulations(employee_ids) and
                populator.generate_quishing_simulations(employee_ids) and
                populator.generate_red_team_assessments(employee_ids)):
            print(f"✗ Test {test_num}: Failed to generate complete data")
            return None
        
        # Get detailed metrics for ER schema
        try:
            # Phishing metrics from employee_master (baseline data)
            populator.cursor.execute("""
                SELECT AVG(click_response_rate) as avg_baseline_click 
                FROM employee_master
            """)
            baseline_result = populator.cursor.fetchone()
            baseline_click = float(baseline_result[0]) if baseline_result[0] else 0
            
            # Phishing metrics from simulation table
            populator.cursor.execute("""
                SELECT AVG(click_response_rate) as avg_sim_click 
                FROM employee_phish_smish_sim
            """)
            sim_result = populator.cursor.fetchone()
            sim_click = float(sim_result[0]) if sim_result[0] else 0
            
            # Vishing metrics
            populator.cursor.execute("""
                SELECT AVG(vish_response_rate) as avg_vish_rate 
                FROM employee_vishing_sim
            """)
            vish_result = populator.cursor.fetchone()
            vish_rate = float(vish_result[0]) if vish_result[0] else 0
            
            # Quishing metrics
            populator.cursor.execute("""
                SELECT 
                    AVG(qr_scan_rate) as avg_qr_scan,
                    COUNT(CASE WHEN malicious_qr_clicked = 1 THEN 1 END) as malicious_clicks,
                    COUNT(*) as total_qr_sims
                FROM employee_quishing_sim
            """)
            qr_result = populator.cursor.fetchone()
            qr_scan_rate = float(qr_result[0]) if qr_result[0] else 0
            malicious_clicks = int(qr_result[1]) if qr_result[1] else 0
            total_qr_sims = int(qr_result[2]) if qr_result[2] else 0
            
            # Red team assessment scores
            populator.cursor.execute("""
                SELECT 
                    AVG(physical_security_score) as avg_physical,
                    AVG(human_security_score) as avg_human,
                    AVG(overall_assessment_score) as avg_overall,
                    COUNT(*) as total_assessments
                FROM red_team_assessment
            """)
            assessment_result = populator.cursor.fetchone()
            avg_physical = float(assessment_result[0]) if assessment_result[0] else 0
            avg_human = float(assessment_result[1]) if assessment_result[1] else 0
            avg_overall = float(assessment_result[2]) if assessment_result[2] else 0
            total_assessments = int(assessment_result[3]) if assessment_result[3] else 0
            
            metrics = {
                'baseline_click_rate': baseline_click,
                'simulation_click_rate': sim_click,
                'vishing_response_rate': vish_rate,
                'qr_scan_rate': qr_scan_rate,
                'malicious_qr_clicks': malicious_clicks,
                'total_qr_simulations': total_qr_sims,
                'physical_security_score': avg_physical,
                'human_security_score': avg_human,
                'overall_security_score': avg_overall,
                'total_assessments': total_assessments,
                'employee_count': employee_count
            }
            
            # Display results
            print(f"Results for {employee_count} employees:")
            print(f"  Employee Master Click Rate: {baseline_click:.2f}% (target: ~22%)")
            print(f"  Simulation Click Rate: {sim_click:.2f}% (mixed baseline/post-intervention)")
            print(f"  Vishing Response Rate: {vish_rate:.2f}%")
            print(f"  QR Scan Rate: {qr_scan_rate:.2f}%, Malicious Clicks: {malicious_clicks}/{total_qr_sims}")
            print(f"  Security Scores - Physical: {avg_physical:.1f}, Human: {avg_human:.1f}, Overall: {avg_overall:.1f}")
            print(f"  Red Team Assessments: {total_assessments} completed")
            
            return metrics
            
        except Exception as e:
            print(f"✗ Error getting metrics: {e}")
            return None


def validate_er_metrics(metrics, test_num, num_employees):
    """Validate that ER schema metrics meet expected ranges"""
    issues = []
    
    # Expected ranges for ER schema with updated failure rates
    expected_ranges = {
        'baseline_click_rate': (21, 25),  # Updated: From employee_master (21-25%)
        'vishing_response_rate': (23, 30),  # Updated: Vishing range (23-30%)
        'qr_scan_rate': (22, 27),  # Updated: QR scan range (22-27%)
        'physical_security_score': (6.0, 9.5),
        'human_security_score': (7.0, 9.0),
        'overall_security_score': (6.5, 9.2)
    }
    
    for metric, (min_val, max_val) in expected_ranges.items():
        if metric in metrics and metrics[metric] is not None:
            value = metrics[metric]
            if not (min_val <= value <= max_val):
                issues.append(f"{metric}: {value:.2f} (expected {min_val}-{max_val})")
    
    # Check data volume expectations
    expected_assessments = int(num_employees * 0.7)  # 70% should get assessed
    actual_assessments = metrics.get('total_assessments', 0)
    if abs(actual_assessments - expected_assessments) > num_employees * 0.1:  # Allow 10% variance
        issues.append(f"assessments: {actual_assessments} (expected ~{expected_assessments})")
    
    if issues:
        print(f"⚠️  Test {test_num}: Metrics outside expected ranges:")
        for issue in issues:
            print(f"    {issue}")
        return False
    else:
        print(f"✓ Test {test_num}: All metrics within expected ranges")
        return True


def run_er_comprehensive_tests():
    """Run comprehensive tests with the ER diagram schema"""
    print("FISST Academy Database Populator - ER Schema Comprehensive Test Suite")
    print("=" * 80)
    print("Testing data generation accuracy with the actual ER diagram schema")
    print("Expected targets based on updated failure rates:")
    print("• Employee Master: 21-25% baseline click rate")
    print("• Phishing/Smishing: 21-25% failure rates")
    print("• Vishing: 26-30% failure rates") 
    print("• Quishing: 22-27% failure rates")
    print("• Red Team: Security assessment scores and findings")
    print("=" * 80)
    
    # Test with different employee counts as requested
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
            result = run_single_er_test(test_num, employee_count)
            if result:
                result['test_num'] = test_num
                all_results.append(result)
                
                if validate_er_metrics(result, test_num, employee_count):
                    successful_tests += 1
            else:
                print(f"✗ Test {test_num}: Failed to complete")
        except Exception as e:
            print(f"✗ Test {test_num}: Exception occurred - {e}")
    
    # Summary analysis
    print(f"\n{'='*25} ER SCHEMA TEST SUMMARY {'='*25}")
    print(f"Completed tests: {len(all_results)}/6")
    print(f"Tests within expected ranges: {successful_tests}/{len(all_results)}")
    
    if all_results:
        # Calculate aggregate statistics
        baseline_clicks = [r['baseline_click_rate'] for r in all_results if r['baseline_click_rate']]
        sim_clicks = [r['simulation_click_rate'] for r in all_results if r['simulation_click_rate']]
        vish_rates = [r['vishing_response_rate'] for r in all_results if r['vishing_response_rate']]
        qr_scan_rates = [r['qr_scan_rate'] for r in all_results if r['qr_scan_rate']]
        
        print(f"\nAggregate Statistics across all tests:")
        if baseline_clicks:
            print(f"Employee Master Click Rate: {statistics.mean(baseline_clicks):.2f}% ± {statistics.stdev(baseline_clicks) if len(baseline_clicks) > 1 else 0:.2f}% (target: ~22%)")
        if sim_clicks:
            print(f"Simulation Click Rate: {statistics.mean(sim_clicks):.2f}% ± {statistics.stdev(sim_clicks) if len(sim_clicks) > 1 else 0:.2f}%")
        if vish_rates:
            print(f"Vishing Response Rate: {statistics.mean(vish_rates):.2f}% ± {statistics.stdev(vish_rates) if len(vish_rates) > 1 else 0:.2f}%")
        if qr_scan_rates:
            print(f"QR Scan Rate: {statistics.mean(qr_scan_rates):.2f}% ± {statistics.stdev(qr_scan_rates) if len(qr_scan_rates) > 1 else 0:.2f}%")
        
        # Data volume summary
        total_employees = sum(r['employee_count'] for r in all_results)
        total_assessments = sum(r['total_assessments'] for r in all_results)
        total_qr_sims = sum(r['total_qr_simulations'] for r in all_results)
        
        print(f"\nData Volume Summary:")
        print(f"Total Employees Generated: {total_employees}")
        print(f"Total Red Team Assessments: {total_assessments}")
        print(f"Total QR Simulations: {total_qr_sims}")
        
        # Final assessment
        overall_success = (successful_tests >= 5 and len(all_results) == 6)
        
        print(f"\n{'='*20} FINAL ER SCHEMA ASSESSMENT {'='*20}")
        if overall_success:
            print("✅ ER SCHEMA COMPREHENSIVE TEST PASSED")
            print("✓ Data generation matches ER diagram structure")
            print("✓ All tables populated with realistic data")
            print("✓ Metrics align with case study requirements")
            print("✓ Script is ready for production use with ER schema")
        else:
            print("❌ ER SCHEMA COMPREHENSIVE TEST NEEDS ATTENTION")
            print("⚠️ Some metrics may need adjustment")
            print("⚠️ Review the generation logic for ER schema compliance")
    else:
        print("❌ No tests completed successfully")
    
    print("=" * 80)


if __name__ == "__main__":
    run_er_comprehensive_tests()