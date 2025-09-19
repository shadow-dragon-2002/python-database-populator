#!/usr/bin/env python3
"""
Simple MySQL Database Populator for FISST Academy
Populates existing tables with realistic fake data.
This is a database population script, not a table creation script.
"""

import mysql.connector
import random
import sys
from faker import Faker
from faker.providers import BaseProvider
from decimal import Decimal
from datetime import datetime, date, timedelta


class IndianDataProvider(BaseProvider):
    """Custom Faker provider for Indian data"""
    
    indian_first_names_male = [
        'Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Sai', 'Reyansh', 'Ayaan', 'Krishna', 'Ishaan',
        'Shaurya', 'Atharv', 'Advik', 'Pranav', 'Rishabh', 'Gokul', 'Rohan', 'Kiran', 'Aryan', 'Advait',
        'Vikram', 'Ankit', 'Rahul', 'Amit', 'Suresh', 'Rajesh', 'Deepak', 'Manoj', 'Ravi', 'Ashok'
    ]
    
    indian_first_names_female = [
        'Saanvi', 'Ananya', 'Diya', 'Aadhya', 'Kiara', 'Anika', 'Avni', 'Sara', 'Myra', 'Aditi',
        'Kavya', 'Sia', 'Ira', 'Pihu', 'Riya', 'Arya', 'Tara', 'Siya', 'Nisha', 'Priya',
        'Meera', 'Pooja', 'Neha', 'Sita', 'Geeta', 'Sunita', 'Kavita', 'Anita', 'Seema', 'Rekha'
    ]
    
    indian_last_names = [
        'Sharma', 'Verma', 'Gupta', 'Agarwal', 'Bansal', 'Garg', 'Jain', 'Mittal', 'Shah', 'Patel',
        'Singh', 'Kumar', 'Yadav', 'Mishra', 'Pandey', 'Tiwari', 'Shukla', 'Dubey', 'Saxena', 'Srivastava'
    ]
    
    indian_cities = [
        'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad',
        'Surat', 'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur', 'Visakhapatnam', 'Indore', 'Thane'
    ]
    
    def indian_name(self):
        gender = random.choice(['M', 'F'])
        if gender == 'M':
            first_name = random.choice(self.indian_first_names_male)
        else:
            first_name = random.choice(self.indian_first_names_female)
        last_name = random.choice(self.indian_last_names)
        return f"{first_name} {last_name}"
    
    def indian_phone(self):
        return f"+91 {random.randint(70, 99)}{random.randint(10000000, 99999999)}"
    
    def indian_city(self):
        return random.choice(self.indian_cities)


class SimpleDatabasePopulator:
    """Simple database populator for FISST Academy data"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.fake = Faker()
        self.fake.add_provider(IndianDataProvider)
        # Use fixed seed for consistent statistics
        random.seed(42)
        Faker.seed(42)
    
    def connect_to_database(self):
        """Connect to MySQL database"""
        print("=== Database Connection ===")
        host = input("Enter host (default: localhost): ").strip() or "localhost"
        port = int(input("Enter port (default: 3306): ").strip() or "3306")
        database = input("Enter database name: ").strip()
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        try:
            self.connection = mysql.connector.connect(
                host=host,
                port=port,
                database=database,
                user=username,
                password=password,
                autocommit=False
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("✓ Successfully connected to MySQL database!")
            return True
        except Exception as e:
            print(f"✗ Failed to connect: {e}")
            return False
    
    def verify_tables_exist(self):
        """Verify that required tables exist"""
        required_tables = [
            'employee_master',
            'employee_phish_smish_sim', 
            'employee_vishing_sim',
            'employee_quishing_sim',
            'red_team_assessment'
        ]
        
        print("\n=== Verifying Tables ===")
        missing_tables = []
        
        for table in required_tables:
            try:
                self.cursor.execute(f"SHOW TABLES LIKE '{table}'")
                if not self.cursor.fetchone():
                    missing_tables.append(table)
            except Exception as e:
                print(f"Error checking table {table}: {e}")
                return False
        
        if missing_tables:
            print(f"❌ Missing tables: {', '.join(missing_tables)}")
            print("Please create these tables first using your SQL schema.")
            return False
        
        print("✓ All required tables found!")
        return True
    
    def clear_existing_data(self):
        """Clear existing data from tables"""
        tables = ['red_team_assessment', 'employee_quishing_sim', 'employee_vishing_sim', 
                  'employee_phish_smish_sim', 'employee_master']
        
        try:
            for table in tables:
                self.cursor.execute(f"DELETE FROM {table}")
            self.connection.commit()
            print("✓ Existing data cleared successfully!")
            return True
        except Exception as e:
            print(f"✗ Error clearing data: {e}")
            self.connection.rollback()
            return False
    
    def generate_employee_data(self, num_employees):
        """Generate employee master data"""
        print(f"\n=== Generating {num_employees} employees ===")
        
        employees_data = []
        used_emails = set()
        
        for i in range(1, num_employees + 1):
            # Generate Indian name
            name_parts = self.fake.indian_name().split()
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else 'Kumar'
            
            # Generate unique emails with @fisstacademy.com
            base_email = f"{first_name.lower()}.{last_name.lower()}"
            work_email = f"{base_email}@fisstacademy.com"
            counter = 1
            while work_email in used_emails:
                work_email = f"{base_email}{counter}@fisstacademy.com"
                counter += 1
            used_emails.add(work_email)
            
            personal_email = f"{base_email}@gmail.com"
            email = work_email  # Primary email
            
            # Generate other data
            gender = random.choice(['M', 'F'])
            date_of_birth = self.fake.date_between(start_date='-65y', end_date='-22y')
            age = 2024 - date_of_birth.year
            blood_group = random.choice(['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'])
            marital_status = random.choice(['Single', 'Married', 'Divorced', 'Widowed'])
            phone_number = self.fake.indian_phone()
            address = f"{random.randint(1, 999)} {random.choice(['MG Road', 'Gandhi Nagar', 'Anna Salai'])}"
            state = random.choice(['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Delhi', 'Gujarat'])
            postal_code = f"{random.randint(100000, 999999)}"
            country = 'India'
            designation = random.choice(['Analyst', 'Manager', 'Senior Analyst', 'Executive', 'Team Lead'])
            department = random.choice(['IT', 'Finance', 'HR', 'Operations', 'Marketing', 'Security'])
            salary = round(random.uniform(25000, 150000), 2)
            work_experience_years = round(random.uniform(0.5, 25.0), 1)
            joining_date = self.fake.date_between(start_date='-10y', end_date='today')
            emergency_contact_name = self.fake.indian_name()
            emergency_contact_phone = self.fake.indian_phone()
            family_details = f"Family of {random.randint(2, 6)} members"
            medical_conditions = random.choice(['None', 'Diabetes', 'Hypertension', 'Asthma', 'None'])
            simulation_type = random.choice(['Phishing', 'Vishing', 'Quishing'])
            
            # Simulation rates with consistent statistics
            base_phish_rate = 23.1
            base_vish_rate = 23.6  
            base_quish_rate = 23.1
            
            click_response_rate = round(random.uniform(base_phish_rate - 2, base_phish_rate + 2), 2)
            phish_last_simulation_date = self.fake.date_between(start_date='-6m', end_date='today')
            phish_testing_status = random.choice(['Completed', 'Scheduled', 'In Progress'])
            
            vishing_phone_number = phone_number
            vishing_alt_phone_number = self.fake.indian_phone()
            voice_auth_test = random.choice([True, False])
            vish_response_rate = round(random.uniform(base_vish_rate - 2, base_vish_rate + 2), 2)
            vish_last_simulation_date = self.fake.date_between(start_date='-6m', end_date='today')
            vish_testing_status = random.choice(['Completed', 'Scheduled', 'In Progress'])
            
            quish_response_rate = round(random.uniform(base_quish_rate - 2, base_quish_rate + 2), 2)
            quish_last_simulation_date = self.fake.date_between(start_date='-6m', end_date='today')
            quish_testing_status = random.choice(['Completed', 'Scheduled', 'In Progress'])
            
            # Red team assessment data
            branch_location = self.fake.indian_city()
            branch_code = f"BR{random.randint(10, 99)}"
            total_employees_at_branch = random.randint(50, 500)
            security_level = random.choice(['High', 'Medium', 'Low'])
            building_storeys = random.randint(1, 20)
            assessment_date = self.fake.date_between(start_date='-3m', end_date='today')
            assessment_time_start = self.fake.time()
            assessment_time_end = self.fake.time()
            permission_granted = random.choice([True, False])
            approving_official_name = self.fake.indian_name()
            approving_official_designation = random.choice(['Manager', 'Director', 'VP'])
            identity_verification_required = True
            identity_verified = random.choice([True, False])
            security_guard_present = random.choice([True, False])
            visitor_log_maintained = True
            badge_issued = random.choice([True, False])
            escort_required = random.choice([True, False])
            restricted_areas_accessed = random.choice([True, False])
            tailgating_possible = random.choice([True, False])
            social_engineering_successful = random.choice([True, False])
            physical_security_score = round(random.uniform(1.0, 10.0), 1)
            human_security_score = round(random.uniform(1.0, 10.0), 1)
            overall_assessment_score = round((physical_security_score + human_security_score) / 2, 1)
            vulnerabilities_found = random.choice(['Weak access controls', 'Social engineering susceptibility', 'None significant'])
            recommendations = random.choice(['Enhanced security training', 'Improve access controls', 'Continue current practices'])
            assessor_name = self.fake.indian_name()
            assessor_id = f"ASST{random.randint(1, 20):02d}"
            notes = f"Assessment completed for {department} department"
            red_team_testing_status = 'Completed'
            organisation_name = 'FISST Academy'
            
            employees_data.append((
                i, first_name, last_name, gender, date_of_birth, age, blood_group, marital_status,
                email, phone_number, address, state, postal_code, country, designation, department,
                salary, work_experience_years, joining_date, emergency_contact_name, emergency_contact_phone,
                family_details, medical_conditions, simulation_type, work_email, personal_email,
                click_response_rate, phish_last_simulation_date, phish_testing_status,
                vishing_phone_number, vishing_alt_phone_number, voice_auth_test, vish_response_rate,
                vish_last_simulation_date, vish_testing_status, quish_response_rate, quish_last_simulation_date,
                quish_testing_status, branch_location, branch_code, total_employees_at_branch, security_level,
                building_storeys, assessment_date, assessment_time_start, assessment_time_end, permission_granted,
                approving_official_name, approving_official_designation, identity_verification_required,
                identity_verified, security_guard_present, visitor_log_maintained, badge_issued, escort_required,
                restricted_areas_accessed, tailgating_possible, social_engineering_successful, physical_security_score,
                human_security_score, overall_assessment_score, vulnerabilities_found, recommendations,
                assessor_name, assessor_id, notes, red_team_testing_status, organisation_name
            ))
        
        try:
            sql = """
            INSERT INTO employee_master (
                employee_id, first_name, last_name, gender, date_of_birth, age, blood_group, marital_status,
                email, phone_number, address, state, postal_code, country, designation, department,
                salary, work_experience_years, joining_date, emergency_contact_name, emergency_contact_phone,
                family_details, medical_conditions, simulation_type, work_email, personal_email,
                click_response_rate, phish_last_simulation_date, phish_testing_status,
                vishing_phone_number, vishing_alt_phone_number, voice_auth_test, vish_response_rate,
                vish_last_simulation_date, vish_testing_status, quish_response_rate, quish_last_simulation_date,
                quish_testing_status, branch_location, branch_code, total_employees_at_branch, security_level,
                building_storeys, assessment_date, assessment_time_start, assessment_time_end, permission_granted,
                approving_official_name, approving_official_designation, identity_verification_required,
                identity_verified, security_guard_present, visitor_log_maintained, badge_issued, escort_required,
                restricted_areas_accessed, tailgating_possible, social_engineering_successful, physical_security_score,
                human_security_score, overall_assessment_score, vulnerabilities_found, recommendations,
                assessor_name, assessor_id, notes, red_team_testing_status, organisation_name
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.executemany(sql, employees_data)
            self.connection.commit()
            print(f"✓ Generated {len(employees_data)} employees!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating employees: {e}")
            self.connection.rollback()
            return False
    
    def generate_simulation_data(self):
        """Generate simulation data for all tables"""
        print("\n=== Generating simulation data ===")
        
        # Get employee data
        self.cursor.execute("SELECT serial_no, employee_id FROM employee_master")
        employees = self.cursor.fetchall()
        
        if not employees:
            print("No employees found!")
            return False
        
        # Generate phishing/smishing data
        self.generate_phishing_data(employees)
        
        # Generate vishing data  
        self.generate_vishing_data(employees)
        
        # Generate quishing data
        self.generate_quishing_data(employees)
        
        # Generate red team assessment data
        self.generate_red_team_data(employees)
        
        return True
    
    def generate_phishing_data(self, employees):
        """Generate phishing simulation data"""
        phish_data = []
        simulation_types = ['Phishing', 'Smishing']
        
        for emp in employees:
            for _ in range(random.randint(1, 3)):
                simulation_type = random.choice(simulation_types)
                work_email = f"emp{emp['employee_id']}@fisstacademy.com"
                personal_email = f"emp{emp['employee_id']}@gmail.com"
                phone_number = self.fake.indian_phone()
                click_response_rate = round(random.uniform(21.0, 25.0), 2)
                last_simulation_date = self.fake.date_between(start_date='-6m', end_date='today')
                testing_status = random.choice(['Completed', 'Scheduled', 'In Progress'])
                
                phish_data.append((
                    emp['serial_no'], emp['employee_id'], simulation_type, work_email, 
                    personal_email, phone_number, click_response_rate, last_simulation_date, testing_status
                ))
        
        sql = """
        INSERT INTO employee_phish_smish_sim (
            serial_no, employee_id, simulation_type, work_email, personal_email, 
            phone_number, click_response_rate, last_simulation_date, testing_status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        self.cursor.executemany(sql, phish_data)
        print(f"✓ Generated {len(phish_data)} phishing simulation entries!")
    
    def generate_vishing_data(self, employees):
        """Generate vishing simulation data"""
        vish_data = []
        
        for emp in employees:
            for _ in range(random.randint(1, 2)):
                phone_number = self.fake.indian_phone()
                alt_phone_number = self.fake.indian_phone()
                voice_auth_test = random.choice([True, False])
                vish_response_rate = round(random.uniform(21.5, 25.5), 2)
                last_simulation = self.fake.date_between(start_date='-6m', end_date='today')
                testing_status = random.choice(['Completed', 'Scheduled', 'In Progress'])
                
                vish_data.append((
                    emp['serial_no'], emp['employee_id'], phone_number, alt_phone_number,
                    voice_auth_test, vish_response_rate, last_simulation, testing_status
                ))
        
        sql = """
        INSERT INTO employee_vishing_sim (
            serial_no, employee_id, phone_number, alt_phone_number, voice_auth_test,
            vish_response_rate, last_simulation, testing_status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        self.cursor.executemany(sql, vish_data)
        print(f"✓ Generated {len(vish_data)} vishing simulation entries!")
    
    def generate_quishing_data(self, employees):
        """Generate quishing simulation data"""
        quish_data = []
        devices = ['Mobile', 'Desktop', 'Tablet']
        locations = ['Office', 'Home', 'Public WiFi', 'Cafe', 'Airport']
        actions = ['Clicked', 'Ignored', 'Reported']
        
        for emp in employees:
            for _ in range(random.randint(1, 2)):
                qr_code_link = f"https://fisst-test.com/qr/{random.randint(1000, 9999)}"
                device_used = random.choice(devices)
                scan_location = random.choice(locations)
                scan_time = self.fake.date_time_between(start_date='-6m', end_date='now')
                response_action = random.choice(actions)
                quish_response_rate = round(random.uniform(21.0, 25.0), 2)
                last_simulation_date = self.fake.date_between(start_date='-6m', end_date='today')
                testing_status = random.choice(['Completed', 'Scheduled', 'In Progress'])
                
                quish_data.append((
                    emp['serial_no'], emp['employee_id'], qr_code_link, device_used, scan_location,
                    scan_time, response_action, quish_response_rate, last_simulation_date, testing_status
                ))
        
        sql = """
        INSERT INTO employee_quishing_sim (
            serial_no, employee_id, qr_code_link, device_used, scan_location, scan_time,
            response_action, quish_response_rate, last_simulation_date, testing_status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        self.cursor.executemany(sql, quish_data)
        print(f"✓ Generated {len(quish_data)} quishing simulation entries!")
    
    def generate_red_team_data(self, employees):
        """Generate red team assessment data"""
        red_team_data = []
        
        for emp in employees:
            branch_location = self.fake.indian_city()
            branch_code = f"BR{random.randint(10, 99)}"
            total_employees_at_branch = random.randint(50, 500)
            security_level = random.choice(['High', 'Medium', 'Low'])
            building_storeys = random.randint(1, 20)
            assessment_date = self.fake.date_between(start_date='-3m', end_date='today')
            assessment_time_start = self.fake.time()
            assessment_time_end = self.fake.time()
            permission_granted = random.choice([True, False])
            approving_official_name = self.fake.indian_name()
            approving_official_designation = random.choice(['Manager', 'Director', 'VP'])
            identity_verification_required = True
            identity_verified = random.choice([True, False])
            security_guard_present = random.choice([True, False])
            visitor_log_maintained = True
            badge_issued = random.choice([True, False])
            escort_required = random.choice([True, False])
            restricted_areas_accessed = random.choice([True, False])
            tailgating_possible = random.choice([True, False])
            social_engineering_successful = random.choice([True, False])
            physical_security_score = round(random.uniform(1.0, 10.0), 1)
            human_security_score = round(random.uniform(1.0, 10.0), 1)
            overall_assessment_score = round((physical_security_score + human_security_score) / 2, 1)
            vulnerabilities_found = random.choice(['Weak access controls', 'Social engineering susceptibility', 'None significant'])
            recommendations = random.choice(['Enhanced security training', 'Improve access controls', 'Continue current practices'])
            assessor_name = self.fake.indian_name()
            assessor_id = f"ASST{random.randint(1, 20):02d}"
            notes = f"Red team assessment completed"
            testing_status = 'Completed'
            
            red_team_data.append((
                emp['serial_no'], emp['employee_id'], branch_location, branch_code, total_employees_at_branch,
                security_level, building_storeys, assessment_date, assessment_time_start, assessment_time_end,
                permission_granted, approving_official_name, approving_official_designation,
                identity_verification_required, identity_verified, security_guard_present, visitor_log_maintained,
                badge_issued, escort_required, restricted_areas_accessed, tailgating_possible,
                social_engineering_successful, physical_security_score, human_security_score,
                overall_assessment_score, vulnerabilities_found, recommendations, assessor_name,
                assessor_id, notes, testing_status
            ))
        
        sql = """
        INSERT INTO red_team_assessment (
            serial_no, employee_id, branch_location, branch_code, total_employees_at_branch,
            security_level, building_storeys, assessment_date, assessment_time_start, assessment_time_end,
            permission_granted, approving_official_name, approving_official_designation,
            identity_verification_required, identity_verified, security_guard_present, visitor_log_maintained,
            badge_issued, escort_required, restricted_areas_accessed, tailgating_possible,
            social_engineering_successful, physical_security_score, human_security_score,
            overall_assessment_score, vulnerabilities_found, recommendations, assessor_name,
            assessor_id, notes, testing_status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        self.cursor.executemany(sql, red_team_data)
        print(f"✓ Generated {len(red_team_data)} red team assessment entries!")
    
    def display_statistics(self):
        """Display data statistics"""
        print("\n=== Data Statistics ===")
        
        # Employee count
        self.cursor.execute("SELECT COUNT(*) as count FROM employee_master")
        emp_count = self.cursor.fetchone()['count']
        print(f"Employees: {emp_count}")
        
        # Simulation counts
        tables = [
            ('Phishing Simulations', 'employee_phish_smish_sim'),
            ('Vishing Simulations', 'employee_vishing_sim'),
            ('Quishing Simulations', 'employee_quishing_sim'),
            ('Red Team Assessments', 'red_team_assessment')
        ]
        
        for name, table in tables:
            self.cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            count = self.cursor.fetchone()['count']
            print(f"{name}: {count}")
        
        # Average response rates
        self.cursor.execute("SELECT AVG(click_response_rate) as avg_rate FROM employee_master")
        phish_avg = self.cursor.fetchone()['avg_rate']
        print(f"Average Phishing Response Rate: {phish_avg:.1f}%")
        
        self.cursor.execute("SELECT AVG(vish_response_rate) as avg_rate FROM employee_master")
        vish_avg = self.cursor.fetchone()['avg_rate']
        print(f"Average Vishing Response Rate: {vish_avg:.1f}%")
        
        self.cursor.execute("SELECT AVG(quish_response_rate) as avg_rate FROM employee_master")
        quish_avg = self.cursor.fetchone()['avg_rate']
        print(f"Average Quishing Response Rate: {quish_avg:.1f}%")
    
    def close_connection(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("\n✓ Database connection closed")


def main():
    """Main function"""
    print("FISST Academy Simple Database Populator")
    print("=" * 50)
    
    populator = SimpleDatabasePopulator()
    
    try:
        # Connect to database
        if not populator.connect_to_database():
            return
        
        # Verify tables exist
        if not populator.verify_tables_exist():
            return
        
        # Check for existing data
        print("\n=== Data Management ===")
        if populator.cursor.execute("SELECT COUNT(*) as count FROM employee_master") or True:
            populator.cursor.execute("SELECT COUNT(*) as count FROM employee_master")
            existing_count = populator.cursor.fetchone()['count']
            if existing_count > 0:
                print(f"Found {existing_count} existing employees.")
                clear_data = input("Clear existing data? (y/n): ").strip().lower()
                if clear_data == 'y':
                    if not populator.clear_existing_data():
                        return
        
        # Get number of employees
        while True:
            try:
                num_employees = int(input("\nEnter number of employees to generate: ").strip())
                if num_employees > 0:
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Generate data
        if not populator.generate_employee_data(num_employees):
            return
        
        if not populator.generate_simulation_data():
            return
        
        # Display statistics
        populator.display_statistics()
        
        print("\n✓ Database population completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
    finally:
        populator.close_connection()


if __name__ == "__main__":
    main()