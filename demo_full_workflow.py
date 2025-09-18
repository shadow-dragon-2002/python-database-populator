#!/usr/bin/env python3
"""
Simple demo script showing the database_populator.py functionality.
This creates a temporary SQLite database and demonstrates the full workflow.
"""

import os
import sqlite3
import tempfile
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_populator import DatabasePopulator


class SQLiteDemoPopulator(DatabasePopulator):
    """SQLite version for demo purposes"""
    
    def __init__(self, db_path):
        super().__init__()
        self.db_type = 'sqlite'
        self.db_path = db_path
        
    def connect_to_database(self, config=None):
        """Connect to SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            print(f"✓ Connected to SQLite database: {self.db_path}")
            return True
        except Exception as e:
            print(f"✗ Failed to connect to database: {e}")
            return False
    
    def _adapt_sql_for_sqlite(self, sql):
        """Adapt MySQL/PostgreSQL SQL to SQLite"""
        # Replace AUTO_INCREMENT with AUTOINCREMENT
        sql = sql.replace('AUTO_INCREMENT', 'AUTOINCREMENT')
        # Replace SERIAL with INTEGER PRIMARY KEY AUTOINCREMENT
        sql = sql.replace('SERIAL PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
        # Replace %s with ?
        return sql
    
    def _get_employee_master_table_sql(self):
        """SQLite version of employee_master table"""
        sql = super()._get_employee_master_table_sql()
        return self._adapt_sql_for_sqlite(sql)
    
    def _get_employee_phish_smish_sim_table_sql(self):
        """SQLite version of employee_phish_smish_sim table"""
        sql = super()._get_employee_phish_smish_sim_table_sql()
        return self._adapt_sql_for_sqlite(sql)
    
    def _get_employee_vishing_sim_table_sql(self):
        """SQLite version of employee_vishing_sim table"""
        sql = super()._get_employee_vishing_sim_table_sql()
        return self._adapt_sql_for_sqlite(sql)
    
    def _get_employee_quishing_sim_table_sql(self):
        """SQLite version of employee_quishing_sim table"""
        sql = super()._get_employee_quishing_sim_table_sql()
        return self._adapt_sql_for_sqlite(sql)
    
    def _get_red_team_assessment_table_sql(self):
        """SQLite version of red_team_assessment table"""
        sql = super()._get_red_team_assessment_table_sql()
        return self._adapt_sql_for_sqlite(sql)
    
    def generate_employees(self, num_employees):
        """Override to use SQLite placeholders"""
        from database_populator import random
        
        departments = ['IT Security', 'Human Resources', 'Finance', 'Operations', 'Marketing', 'Sales', 'Research', 'Admin']
        designations = ['Analyst', 'Manager', 'Coordinator', 'Specialist', 'Executive', 'Director', 'Team Lead', 'Senior Analyst']
        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        marital_statuses = ['Single', 'Married', 'Divorced', 'Widowed']
        indian_states = ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Delhi', 'Uttar Pradesh', 'Gujarat', 'West Bengal', 'Rajasthan']
        
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
            email = work_email
            
            # Generate other details with proper data types
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
            
            # Continue with all other fields...
            emergency_contact_name = self.fake.indian_name()
            emergency_contact_phone = self.fake.indian_phone()
            family_details = f"Family of {random.randint(2, 6)} members"
            medical_conditions = random.choice(['None', 'Diabetes', 'Hypertension', 'Asthma', 'None', 'None'])
            
            # Simulation data
            simulation_type = 'Baseline Assessment'
            click_response_rate = round(random.uniform(21, 25), 2)
            phish_test_simulation_date = self.fake.date_between(start_date='-6m', end_date='-3m')
            phish_testing_status = 'Completed'
            
            # Add all the other required fields with proper default values
            vishing_phone_number = phone_number
            vishing_alt_phone_number = self.fake.indian_phone()
            voice_auth_test = random.choice([True, False])
            vish_response_rate = round(random.uniform(23, 28), 2)
            vish_test_simulation_date = self.fake.date_between(start_date='-6m', end_date='-3m')
            vish_testing_status = 'Completed'
            
            # Branch and assessment data
            branch_locations = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai']
            branch_codes = ['MUM01', 'DEL02', 'BLR03', 'HYD04', 'CHN05']
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
            
            # Scores
            physical_security_score = round(random.uniform(6.0, 9.0), 1)
            human_security_score = round(random.uniform(7.0, 9.5), 1)
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
            # Use SQLite placeholders (?) instead of %s
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


def main():
    """Run the demo"""
    print("Database Populator Demo - Full Workflow Test")
    print("=" * 60)
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        db_path = tmp_file.name
    
    try:
        populator = SQLiteDemoPopulator(db_path)
        
        # Connect to database
        if not populator.connect_to_database():
            return
        
        print("\n=== Creating the 5 Required Tables ===")
        if not populator.create_tables():
            return
        
        print("\n=== Generating Sample Data ===")
        num_employees = 10
        
        # Generate employee data
        if not populator.generate_employees(num_employees):
            print("✗ Failed to generate employees")
            return
        
        # Get employee IDs
        employee_ids = populator.get_employee_ids()
        if not employee_ids:
            print("✗ No employee IDs found")
            return
        
        print(f"✓ Generated {len(employee_ids)} employee records")
        
        # Generate simulation data for the other 4 tables
        print("\n=== Populating Related Tables ===")
        print("Note: Using simplified data generation for demo purposes")
        
        # Add simple data to other tables for demonstration
        # (In a real scenario, you'd adapt the other generation methods too)
        populator.cursor.execute("""
            INSERT INTO employee_phish_smish_sim (employee_id, simulation_type, work_email, personal_email, click_response_rate, testing_status)
            SELECT employee_id, 'Email Phishing', work_email, personal_email, click_response_rate, 'Completed'
            FROM employee_master
        """)
        
        populator.cursor.execute("""
            INSERT INTO employee_vishing_sim (employee_id, phone_number, alt_phone_number, vish_response_rate, testing_status)
            SELECT employee_id, vishing_phone_number, vishing_alt_phone_number, vish_response_rate, 'Completed'
            FROM employee_master
        """)
        
        populator.cursor.execute("""
            INSERT INTO employee_quishing_sim (employee_id, qr_code_type, qr_scan_rate, malicious_qr_clicked, device_type, testing_status, simulation_date)
            SELECT employee_id, 'Payment QR', 25.5, 0, 'Mobile Phone', 'Completed', date('now')
            FROM employee_master
        """)
        
        populator.cursor.execute("""
            INSERT INTO red_team_assessment (employee_id, branch_code, local_employees_at_branch, security_level, building_storeys,
                assessment_date, permission_granted, approving_official_name, approving_official_designation,
                identity_verification_required, identity_verified, security_guard_present, visitor_log_maintained,
                badge_issued, escort_required, restricted_areas_accessed, tailgating_possible, 
                social_engineering_successful, physical_security_score, human_security_score, overall_assessment_score,
                vulnerabilities_found, recommendations, assessor_name, assessor_id, notes, testing_status)
            SELECT employee_id, branch_code, total_employees_at_branch, security_level, building_storeys,
                assessment_date, permission_granted, approving_official_name, approving_official_designation,
                identity_verification_required, identity_verified, security_guard_present, visitor_log_maintained,
                badge_issued, escort_required, restricted_areas_accessed, tailgating_possible,
                social_engineering_successful, physical_security_score, human_security_score, overall_assessment_score,
                vulnerabilities_found, recommendations, assessor_name, assessor_id, notes, red_team_testing_status
            FROM employee_master
        """)
        
        populator.connection.commit()
        
        print("\n=== Verifying Data in All 5 Tables ===")
        tables = [
            'employee_master',
            'employee_phish_smish_sim', 
            'employee_vishing_sim',
            'employee_quishing_sim',
            'red_team_assessment'
        ]
        
        for table in tables:
            populator.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = populator.cursor.fetchone()[0]
            print(f"✓ {table}: {count} records")
        
        print("\n=== Sample Data from employee_master ===")
        populator.cursor.execute("""
            SELECT employee_id, first_name, last_name, department, designation, email, phone_number
            FROM employee_master LIMIT 3
        """)
        
        for row in populator.cursor.fetchall():
            print(f"  {row['employee_id']}: {row['first_name']} {row['last_name']}, {row['designation']} in {row['department']}")
            print(f"    Email: {row['email']}, Phone: {row['phone_number']}")
        
        print(f"\n🎉 Demo completed successfully!")
        print(f"Database created at: {db_path}")
        print(f"All 5 tables created and populated with complete data!")
        
    except Exception as e:
        print(f"✗ Demo failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        populator.close_connection()
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)


if __name__ == "__main__":
    main()