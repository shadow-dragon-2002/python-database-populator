#!/usr/bin/env python3
"""
MySQL Database Populator for FISST Academy Cybersecurity Simulation
Populates existing tables with realistic fake data based on the provided schema.
"""

import mysql.connector
import random
import sys
from faker import Faker
from faker.providers import BaseProvider
from decimal import Decimal
from datetime import datetime, date, timedelta
import time


class IndianDataProvider(BaseProvider):
    """Custom Faker provider for Indian data"""
    
    # Common Indian first names
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
    
    # Common Indian surnames
    indian_last_names = [
        'Sharma', 'Verma', 'Gupta', 'Agarwal', 'Bansal', 'Garg', 'Jain', 'Mittal', 'Shah', 'Patel',
        'Singh', 'Kumar', 'Yadav', 'Mishra', 'Pandey', 'Tiwari', 'Shukla', 'Dubey', 'Saxena', 'Srivastava',
        'Chandra', 'Iyer', 'Nair', 'Reddy', 'Rao', 'Pillai', 'Menon', 'Das', 'Roy', 'Ghosh'
    ]
    
    # Indian cities
    indian_cities = [
        'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad',
        'Surat', 'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur', 'Visakhapatnam', 'Indore', 'Thane',
        'Bhopal', 'Patna', 'Vadodara', 'Ghaziabad', 'Ludhiana', 'Coimbatore', 'Madurai', 'Vijayawada'
    ]
    
    # Indian street name components
    indian_street_components = [
        'MG Road', 'Gandhi Nagar', 'Nehru Street', 'Rajaji Road', 'Anna Salai', 'Brigade Road',
        'Commercial Street', 'Park Street', 'Church Street', 'Ring Road', 'Civil Lines', 'Model Town'
    ]
    
    def indian_name(self):
        """Generate a random Indian name"""
        if random.choice([True, False]):
            first_name = self.random_element(self.indian_first_names_male)
        else:
            first_name = self.random_element(self.indian_first_names_female)
        last_name = self.random_element(self.indian_last_names)
        return f"{first_name} {last_name}"
    
    def indian_city(self):
        """Generate a random Indian city"""
        return self.random_element(self.indian_cities)
    
    def indian_phone(self):
        """Generate a random Indian phone number"""
        return f"+91 {random.randint(7000000000, 9999999999)}"
    
    def street_name(self):
        """Generate a random Indian street name"""
        return self.random_element(self.indian_street_components)


class DatabasePopulator:
    """Main class for database population and management"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.fake = Faker()
        self.fake.add_provider(IndianDataProvider)
    
    def get_database_config(self):
        """Get database connection details from user"""
        print("=== MySQL Database Connection Configuration ===")
        print("📋 Make sure your MySQL database server is running and accessible.")
        print("📋 Ensure the required tables already exist in your database.")
        print("")
        
        # Get connection details with validation
        while True:
            host = input("Enter host (default: localhost): ").strip() or "localhost"
            
            port_input = input("Enter port (default: 3306): ").strip()
            try:
                port = int(port_input) if port_input else 3306
                if port < 1 or port > 65535:
                    print("❌ Port must be between 1 and 65535")
                    continue
            except ValueError:
                print("❌ Port must be a valid number")
                continue
            
            database = input("Enter database name: ").strip()
            if not database:
                print("❌ Database name cannot be empty")
                continue
                
            username = input("Enter username: ").strip()
            if not username:
                print("❌ Username cannot be empty")
                continue
                
            password = input("Enter password: ").strip()
            
            # Confirmation
            print(f"\n📋 Connection Details:")
            print(f"   Host: {host}")
            print(f"   Port: {port}")
            print(f"   Database: {database}")
            print(f"   Username: {username}")
            print(f"   Password: {'*' * len(password) if password else '(empty)'}")
            
            confirm = input("\nProceed with these settings? (y/n): ").lower().strip()
            if confirm in ['y', 'yes']:
                break
            elif confirm in ['n', 'no']:
                print("Let's reconfigure...\n")
                continue
            else:
                print("Please enter 'y' for yes or 'n' for no")
        
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
            self.connection = mysql.connector.connect(
                host=config['host'],
                port=config['port'],
                database=config['database'],
                user=config['username'],
                password=config['password'],
                connect_timeout=10
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print(f"✓ Successfully connected to MySQL database!")
            return True
            
        except Exception as e:
            self._handle_connection_error(e, config)
            return False
    
    def _handle_connection_error(self, error, config):
        """Handle database connection errors with helpful troubleshooting information"""
        error_str = str(error)
        print(f"✗ Failed to connect to database: {error}")
        print("\n🔧 Troubleshooting Guide:")
        
        if "Access denied" in error_str:
            print("❌ Authentication Error:")
            print(f"   • Check if username '{config['username']}' is correct")
            print("   • Verify the password is correct")
            print("   • Ensure the user has appropriate database privileges")
            print("   • For MySQL, try running: GRANT ALL PRIVILEGES ON *.* TO 'username'@'%';")
            
        elif "Can't connect" in error_str or "Connection refused" in error_str:
            print("❌ Connection Error:")
            print(f"   • Check if MySQL server is running on {config['host']}:{config['port']}")
            print("   • Verify the host IP address/hostname is correct")
            print("   • Check firewall settings and network connectivity")
            print("   • For local testing, try host='localhost' or '127.0.0.1'")
            
        elif "Unknown database" in error_str:
            print("❌ Database Not Found:")
            print(f"   • Database '{config['database']}' does not exist")
            print("   • Create the database first or use an existing database name")
            print(f"   • For MySQL: CREATE DATABASE {config['database']};")
        
        print(f"\n💡 Quick Solutions:")
        print("   • For local MySQL: Use host='localhost', user='root'")
        print("   • For remote MySQL: Ensure user has remote access privileges")
        print("   • Try: mysql -h {host} -u {username} -p {database}")
    
    def verify_tables_exist(self):
        """Verify that all required tables exist in the database"""
        required_tables = [
            'employee_master',
            'employee_phish_smish_sim',
            'employee_vishing_sim',
            'employee_quishing_sim',
            'red_team_assessment'
        ]
        
        existing_tables = []
        missing_tables = []
        
        try:
            for table in required_tables:
                self.cursor.execute(f"SHOW TABLES LIKE '{table}'")
                result = self.cursor.fetchone()
                if result:
                    existing_tables.append(table)
                else:
                    missing_tables.append(table)
            
            if missing_tables:
                print(f"❌ Missing required tables: {', '.join(missing_tables)}")
                print("📋 Please create these tables first using the provided SQL schema.")
                return False
            else:
                print(f"✓ All required tables found: {', '.join(existing_tables)}")
                return True
                
        except Exception as e:
            print(f"✗ Error checking tables: {e}")
            return False
    
    def check_data_exists(self):
        """Check if data exists in any of the tables"""
        tables = ['employee_master', 'employee_phish_smish_sim', 'employee_vishing_sim', 'employee_quishing_sim', 'red_team_assessment']
        
        try:
            for table in tables:
                self.cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                result = self.cursor.fetchone()
                count = result['count']
                if count > 0:
                    return True
            return False
        except Exception as e:
            print(f"Error checking data existence: {e}")
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
                count = result['count']
                print(f"{table_name.replace('_', ' ').title()}: {count} records")
            except Exception as e:
                print(f"{table_name}: Error - {e}")
    
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
    
    def generate_consistent_statistics(self, num_employees):
        """Generate consistent statistics regardless of employee count"""
        import random as stats_random
        stats_random.seed(42)  # Fixed seed for consistent results
        
        # Base percentages that should remain consistent
        base_stats = {
            'phishing_click_rate': 22.5,  # Average around 22.5%
            'vishing_response_rate': 25.5,  # Average around 25.5%
            'quishing_scan_rate': 24.0,   # Average around 24.0%
            'physical_security_score': 7.5,  # Average around 7.5/10
            'human_security_score': 8.0,    # Average around 8.0/10
        }
        
        # Generate slight variations around base values
        variations = {}
        for key, base_value in base_stats.items():
            variation = stats_random.uniform(-2.0, 2.0)  # ±2% variation
            variations[key] = max(0, min(100, base_value + variation))
        
        return variations
    
    def generate_employees(self, num_employees):
        """Generate employee master data according to the new schema"""
        # Get consistent statistics for this run
        consistent_stats = self.generate_consistent_statistics(num_employees)
        
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
            employee_id = i + 1  # Integer employee_id starting from 1
            
            # Generate Indian name components
            name_parts = self.fake.indian_name().split()
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else 'Kumar'
            
            # Generate unique emails
            base_work_email = f"{first_name.lower()}.{last_name.lower()}"
            work_email = f"{base_work_email}@fisstacademy.com"
            counter = 1
            while work_email in used_emails:
                work_email = f"{base_work_email}{counter}@fisstacademy.com"
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
            salary = round(random.uniform(300000, 2000000), 2)
            work_experience_years = round(random.uniform(0.5, 20.0), 1)
            joining_date = self.fake.date_between(start_date='-10y', end_date='today')
            
            # Emergency contact
            emergency_contact_name = self.fake.indian_name()
            emergency_contact_phone = self.fake.indian_phone()
            
            # Family and medical details
            family_details = f"Family of {random.randint(2, 6)} members"
            medical_conditions = random.choice(['None', 'Diabetes', 'Hypertension', 'Asthma', 'None', 'None'])
            
            # Simulation type
            simulation_type = 'Baseline Assessment'
            
            # Use consistent statistics with small individual variations
            base_click_rate = consistent_stats['phishing_click_rate']
            click_response_rate = round(random.uniform(base_click_rate - 1, base_click_rate + 1), 2)
            phish_last_simulation_date = self.fake.date_between(start_date='-6m', end_date='-3m')
            phish_testing_status = 'Completed'
            
            # Vishing data with consistent stats
            vishing_phone_number = phone_number
            vishing_alt_phone_number = self.fake.indian_phone()
            voice_auth_test = random.choice([True, False])
            base_vish_rate = consistent_stats['vishing_response_rate']
            vish_response_rate = round(random.uniform(base_vish_rate - 1, base_vish_rate + 1), 2)
            vish_last_simulation_date = self.fake.date_between(start_date='-6m', end_date='-3m')
            vish_testing_status = 'Completed'
            
            # Quishing data
            base_quish_rate = consistent_stats['quishing_scan_rate']
            quish_response_rate = round(random.uniform(base_quish_rate - 1, base_quish_rate + 1), 2)
            quish_last_simulation_date = self.fake.date_between(start_date='-6m', end_date='-3m')
            quish_testing_status = 'Completed'
            
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
            
            # Use consistent scores with small variations
            base_physical = consistent_stats['physical_security_score']
            base_human = consistent_stats['human_security_score']
            physical_security_score = round(random.uniform(base_physical - 0.5, base_physical + 0.5), 1)
            human_security_score = round(random.uniform(base_human - 0.5, base_human + 0.5), 1)
            overall_assessment_score = round((physical_security_score + human_security_score) / 2, 1)
            
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
            organisation_name = 'FISST Academy'
            
            employees_data.append((
                employee_id, first_name, last_name, gender, date_of_birth, age, blood_group, marital_status,
                email, phone_number, address, state, postal_code, country, designation, department,
                salary, work_experience_years, joining_date, emergency_contact_name, emergency_contact_phone,
                family_details, medical_conditions, simulation_type, work_email, personal_email,
                click_response_rate, phish_last_simulation_date, phish_testing_status,
                vishing_phone_number, vishing_alt_phone_number, voice_auth_test, vish_response_rate,
                vish_last_simulation_date, vish_testing_status,
                quish_response_rate, quish_last_simulation_date, quish_testing_status,
                branch_location, branch_code, total_employees_at_branch, security_level, building_storeys,
                assessment_date, assessment_time_start, assessment_time_end, permission_granted, 
                approving_official_name, approving_official_designation, identity_verification_required, 
                identity_verified, security_guard_present, visitor_log_maintained, badge_issued, 
                escort_required, restricted_areas_accessed, tailgating_possible, social_engineering_successful,
                physical_security_score, human_security_score, overall_assessment_score,
                vulnerabilities_found, recommendations, assessor_name, assessor_id, notes, 
                red_team_testing_status, organisation_name
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
                vish_last_simulation_date, vish_testing_status,
                quish_response_rate, quish_last_simulation_date, quish_testing_status,
                branch_location, branch_code, total_employees_at_branch, security_level, building_storeys,
                assessment_date, assessment_time_start, assessment_time_end, permission_granted, 
                approving_official_name, approving_official_designation, identity_verification_required, 
                identity_verified, security_guard_present, visitor_log_maintained, badge_issued, 
                escort_required, restricted_areas_accessed, tailgating_possible, social_engineering_successful,
                physical_security_score, human_security_score, overall_assessment_score,
                vulnerabilities_found, recommendations, assessor_name, assessor_id, notes, 
                red_team_testing_status, organisation_name
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.executemany(sql, employees_data)
            self.connection.commit()
            print(f"✓ Generated {num_employees} employees in employee_master table!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating employees: {e}")
            self.connection.rollback()
            return False
    
    def get_employee_ids(self):
        """Get list of employee IDs and serial numbers"""
        try:
            self.cursor.execute("SELECT serial_no, employee_id FROM employee_master")
            results = self.cursor.fetchall()
            return [(row['serial_no'], row['employee_id']) for row in results]
        except Exception as e:
            print(f"Error fetching employee IDs: {e}")
            return []
    
    def generate_phish_smish_simulations(self, employee_data):
        """Generate phishing/smishing simulation data"""
        consistent_stats = self.generate_consistent_statistics(len(employee_data))
        base_click_rate = consistent_stats['phishing_click_rate']
        
        sim_data = []
        simulation_types = ['Email', 'SMS']
        testing_statuses = ['Completed', 'Pending', 'Failed', 'Passed']
        
        for serial_no, employee_id in employee_data:
            # Generate multiple simulation entries per employee
            for _ in range(random.randint(2, 4)):
                simulation_type = random.choice(simulation_types)
                work_email = f"emp{employee_id}@fisstacademy.com"
                personal_email = f"emp{employee_id}@gmail.com"
                phone_number = self.fake.indian_phone()
                
                # Use consistent statistics with small individual variations
                click_response_rate = round(random.uniform(base_click_rate - 1.5, base_click_rate + 1.5), 2)
                last_simulation_date = self.fake.date_between(start_date='-6m', end_date='today')
                testing_status = random.choice(testing_statuses)
                
                sim_data.append((
                    serial_no, employee_id, simulation_type, work_email, personal_email,
                    phone_number, click_response_rate, last_simulation_date, testing_status
                ))
        
        try:
            sql = """
            INSERT INTO employee_phish_smish_sim (
                serial_no, employee_id, simulation_type, work_email, personal_email, 
                phone_number, click_response_rate, last_simulation_date, testing_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.executemany(sql, sim_data)
            self.connection.commit()
            print(f"✓ Generated {len(sim_data)} phishing/smishing simulation entries!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating phish/smish simulations: {e}")
            self.connection.rollback()
            return False
    
    def generate_vishing_simulations(self, employee_data):
        """Generate vishing simulation data"""
        consistent_stats = self.generate_consistent_statistics(len(employee_data))
        base_vish_rate = consistent_stats['vishing_response_rate']
        
        sim_data = []
        testing_statuses = ['Completed', 'Pending', 'Failed', 'Passed']
        
        for serial_no, employee_id in employee_data:
            # Generate vishing simulation entries
            for _ in range(random.randint(1, 3)):
                phone_number = self.fake.indian_phone()
                alt_phone_number = self.fake.indian_phone()
                voice_auth_test = random.choice([True, False])
                
                # Use consistent statistics with small individual variations
                vish_response_rate = round(random.uniform(base_vish_rate - 1.5, base_vish_rate + 1.5), 2)
                last_simulation = self.fake.date_between(start_date='-6m', end_date='today')
                testing_status = random.choice(testing_statuses)
                
                sim_data.append((
                    serial_no, employee_id, phone_number, alt_phone_number, voice_auth_test,
                    vish_response_rate, last_simulation, testing_status
                ))
        
        try:
            sql = """
            INSERT INTO employee_vishing_sim (
                serial_no, employee_id, phone_number, alt_phone_number, voice_auth_test,
                vish_response_rate, last_simulation, testing_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.executemany(sql, sim_data)
            self.connection.commit()
            print(f"✓ Generated {len(sim_data)} vishing simulation entries!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating vishing simulations: {e}")
            self.connection.rollback()
            return False
    
    def generate_quishing_simulations(self, employee_data):
        """Generate quishing simulation data"""
        consistent_stats = self.generate_consistent_statistics(len(employee_data))
        base_qr_scan_rate = consistent_stats['quishing_scan_rate']
        
        sim_data = []
        qr_links = [
            'https://fake-payment.com/qr123',
            'https://fake-wifi.com/connect',
            'https://fake-survey.com/form456',
            'https://fake-menu.com/restaurant',
            'https://fake-download.com/app789'
        ]
        devices = ['Mobile', 'Desktop', 'Tablet']
        locations = ['Office', 'Cafe', 'Home', 'Mall', 'Restaurant']
        response_actions = ['Clicked', 'Ignored', 'Reported']
        testing_statuses = ['Completed', 'Pending', 'Failed', 'Passed']
        
        for serial_no, employee_id in employee_data:
            # Generate quishing simulation entries
            for _ in range(random.randint(1, 2)):
                qr_code_link = random.choice(qr_links)
                device_used = random.choice(devices)
                scan_location = random.choice(locations)
                scan_time = self.fake.date_time_between(start_date='-6m', end_date='now')
                response_action = random.choice(response_actions)
                
                # Use consistent statistics with small individual variations
                quish_response_rate = round(random.uniform(base_qr_scan_rate - 1.5, base_qr_scan_rate + 1.5), 2)
                last_simulation_date = self.fake.date_between(start_date='-6m', end_date='today')
                testing_status = random.choice(testing_statuses)
                
                sim_data.append((
                    serial_no, employee_id, qr_code_link, device_used, scan_location, scan_time,
                    response_action, quish_response_rate, last_simulation_date, testing_status
                ))
        
        try:
            sql = """
            INSERT INTO employee_quishing_sim (
                serial_no, employee_id, qr_code_link, device_used, scan_location, scan_time,
                response_action, quish_response_rate, last_simulation_date, testing_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.executemany(sql, sim_data)
            self.connection.commit()
            print(f"✓ Generated {len(sim_data)} quishing simulation entries!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating quishing simulations: {e}")
            self.connection.rollback()
            return False
    
    def generate_red_team_assessments(self, employee_data):
        """Generate red team assessment data"""
        consistent_stats = self.generate_consistent_statistics(len(employee_data))
        
        assessment_data = []
        security_levels = ['Low', 'Medium', 'High', 'Critical']
        testing_statuses = ['Completed', 'In Progress', 'Scheduled', 'Cancelled']
        branch_codes = ['MUM01', 'DEL02', 'BLR03', 'HYD04', 'CHN05', 'KOL06', 'PUN07', 'AHM08']
        branch_locations = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']
        
        for serial_no, employee_id in employee_data:
            # Generate assessment entries (not every employee gets assessed)
            if random.random() < 0.7:  # 70% of employees get assessed
                branch_idx = (employee_id - 1) % len(branch_codes)
                branch_location = branch_locations[branch_idx]
                branch_code = branch_codes[branch_idx]
                total_employees_at_branch = random.randint(15, 50)
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
                
                # Use consistent scores with small variations
                base_physical = consistent_stats['physical_security_score']
                base_human = consistent_stats['human_security_score']
                physical_security_score = round(random.uniform(base_physical - 0.5, base_physical + 0.5), 1)
                human_security_score = round(random.uniform(base_human - 0.5, base_human + 0.5), 1)
                overall_assessment_score = round((physical_security_score + human_security_score) / 2, 1)
                
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
                notes = f"Assessment completed for employee {employee_id}"
                testing_status = random.choice(testing_statuses)
                
                assessment_data.append((
                    serial_no, employee_id, branch_location, branch_code, total_employees_at_branch,
                    security_level, building_storeys, assessment_date, assessment_time_start, assessment_time_end,
                    permission_granted, approving_official_name, approving_official_designation,
                    identity_verification_required, identity_verified, security_guard_present, visitor_log_maintained,
                    badge_issued, escort_required, restricted_areas_accessed, tailgating_possible,
                    social_engineering_successful, physical_security_score, human_security_score, 
                    overall_assessment_score, vulnerabilities_found, recommendations, assessor_name, 
                    assessor_id, notes, testing_status
                ))
        
        try:
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
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.executemany(sql, assessment_data)
            self.connection.commit()
            print(f"✓ Generated {len(assessment_data)} red team assessment entries!")
            return True
            
        except Exception as e:
            print(f"✗ Error generating red team assessments: {e}")
            self.connection.rollback()
            return False
    
    def display_statistics_summary(self):
        """Display comprehensive statistics summary"""
        print("\n=== Generated Data Statistics Summary ===")
        
        try:
            # Employee statistics
            self.cursor.execute("SELECT COUNT(*) as count FROM employee_master")
            employee_count = self.cursor.fetchone()['count']
            print(f"Total Employees: {employee_count}")
            
            # Phishing statistics
            self.cursor.execute("""
                SELECT 
                    AVG(click_response_rate) as avg_click_rate,
                    COUNT(*) as total_phish_sims
                FROM employee_phish_smish_sim
            """)
            phish_metrics = self.cursor.fetchone()
            if phish_metrics:
                avg_click = phish_metrics['avg_click_rate']
                total_phish = phish_metrics['total_phish_sims']
                print(f"Phishing Simulations: {total_phish} total")
                print(f"Average Click Rate: {avg_click:.1f}%")
            
            # Vishing statistics
            self.cursor.execute("""
                SELECT 
                    AVG(vish_response_rate) as avg_vish_rate,
                    COUNT(*) as total_vish_sims
                FROM employee_vishing_sim
            """)
            vish_metrics = self.cursor.fetchone()
            if vish_metrics:
                avg_vish = vish_metrics['avg_vish_rate']
                total_vish = vish_metrics['total_vish_sims']
                print(f"Vishing Simulations: {total_vish} total")
                print(f"Average Response Rate: {avg_vish:.1f}%")
            
            # Quishing statistics
            self.cursor.execute("""
                SELECT 
                    AVG(quish_response_rate) as avg_qr_scan_rate,
                    COUNT(*) as total_quishing_sims
                FROM employee_quishing_sim
            """)
            quish_metrics = self.cursor.fetchone()
            if quish_metrics:
                avg_qr_scan = quish_metrics['avg_qr_scan_rate']
                total_quish = quish_metrics['total_quishing_sims']
                print(f"Quishing Simulations: {total_quish} total")
                print(f"QR Scan Rate: {avg_qr_scan:.1f}%")
            
            # Red team assessment statistics
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
                avg_physical = assessment_metrics['avg_physical_score']
                avg_human = assessment_metrics['avg_human_score']
                avg_overall = assessment_metrics['avg_overall_score']
                total_assessments = assessment_metrics['total_assessments']
                print(f"Red Team Assessments: {total_assessments} total")
                print(f"Physical Security Score: {avg_physical:.1f}/10")
                print(f"Human Security Score: {avg_human:.1f}/10")
                print(f"Overall Assessment Score: {avg_overall:.1f}/10")
            
        except Exception as e:
            print(f"Error generating statistics: {e}")
    
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
    print("FISST Academy MySQL Database Populator")
    print("=" * 50)
    print("🚀 This script populates existing MySQL tables with realistic cybersecurity simulation data.")
    print("📋 Make sure your MySQL database tables are already created using the provided schema.")
    print("")
    
    populator = DatabasePopulator()
    
    try:
        # Get database configuration
        config = populator.get_database_config()
        
        # Connect to database
        if not populator.connect_to_database(config):
            return
        
        # Verify tables exist
        if not populator.verify_tables_exist():
            print("\n❌ Required tables are missing. Please create them first using the provided SQL schema.")
            return
        
        # Check if data exists
        data_exists = populator.check_data_exists()
        
        if data_exists:
            print("\n⚠️  Data already exists in the database tables.")
            populator.display_existing_data()
            
            delete_data = get_yes_no_input("\nDo you want to delete all existing data?")
            
            if delete_data:
                if not populator.delete_all_data():
                    print("❌ Failed to delete existing data.")
                    return
                
                generate_new = get_yes_no_input("Do you want to generate fresh data?")
                if not generate_new:
                    print("✅ Data deleted. Exiting...")
                    return
            else:
                print("✅ Keeping existing data. Exiting...")
                return
        
        # Generate data flow
        while True:
            try:
                num_employees = int(input("\nEnter the number of employees to create: "))
                if num_employees > 0:
                    break
                else:
                    print("Please enter a positive number")
            except ValueError:
                print("Please enter a valid number")
        
        print(f"\n🎯 Generating data for {num_employees} employees...")
        print("📊 Using consistent statistics to ensure reliable reporting metrics...")
        
        # Generate all data
        if populator.generate_employees(num_employees):
            employee_data = populator.get_employee_ids()
            
            if (populator.generate_phish_smish_simulations(employee_data) and
                populator.generate_vishing_simulations(employee_data) and
                populator.generate_quishing_simulations(employee_data) and
                populator.generate_red_team_assessments(employee_data)):
                
                print("\n✅ All data generated successfully!")
                populator.display_statistics_summary()
            else:
                print("\n❌ Some data generation failed")
        else:
            print("\n❌ Employee generation failed")
    
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Please check your database connection and table schema.")
    finally:
        populator.close_connection()


if __name__ == "__main__":
    main()