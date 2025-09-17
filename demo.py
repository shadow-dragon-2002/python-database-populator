#!/usr/bin/env python3
"""
Demo script showing the database_populator.py functionality and user interaction flow.
This demonstrates the script behavior without requiring actual database connections.
"""

from database_populator import DatabasePopulator, get_yes_no_input, IndianDataProvider
from faker import Faker
import random
from decimal import Decimal


def demo_indian_data_generation():
    """Demonstrate Indian data generation"""
    print("=== Indian Data Generation Demo ===")
    
    fake = Faker()
    fake.add_provider(IndianDataProvider)
    
    print("Sample Indian Employee Data:")
    for i in range(5):
        employee_id = f"FISST{str(i+1).zfill(4)}"
        name = fake.indian_name()
        email = f"{name.lower().replace(' ', '.')}@fisst.edu"
        phone = fake.indian_phone()
        city = fake.indian_city()
        department = random.choice(['IT Security', 'Human Resources', 'Finance', 'Operations'])
        
        print(f"  {employee_id}: {name}")
        print(f"    Email: {email}")
        print(f"    Phone: {phone}")
        print(f"    City: {city}")
        print(f"    Department: {department}")
        print()


def demo_security_metrics():
    """Demonstrate security metrics generation logic"""
    print("=== Security Metrics Demo ===")
    
    print("Baseline Metrics (Before Intervention):")
    baseline_clicks = []
    for i in range(10):
        click_rate = random.uniform(20, 24)  # Around 22%
        baseline_clicks.append(click_rate)
        print(f"  Employee {i+1}: {click_rate:.1f}% click rate, 0% reporting")
    
    print(f"\nBaseline Average: {sum(baseline_clicks)/len(baseline_clicks):.1f}% click rate")
    
    print("\nPost-Intervention Metrics:")
    post_clicks = []
    post_reports = []
    for i in range(10):
        click_rate = random.uniform(3, 7)  # Around 5%
        report_rate = random.uniform(35, 41)  # Around 38%
        post_clicks.append(click_rate)
        post_reports.append(report_rate)
        print(f"  Employee {i+1}: {click_rate:.1f}% click rate, {report_rate:.1f}% reporting")
    
    print(f"\nPost-Intervention Average: {sum(post_clicks)/len(post_clicks):.1f}% click rate, {sum(post_reports)/len(post_reports):.1f}% reporting")


def demo_roi_calculation():
    """Demonstrate ROI calculation"""
    print("=== ROI Calculation Demo ===")
    
    engagement_cost = Decimal('48666666.67')  # ₹48.67 lakh
    avoided_fraud = Decimal('730000000.00')  # ₹7.3 crore
    roi_multiple = avoided_fraud / engagement_cost
    
    print(f"Engagement Cost: ₹{float(engagement_cost)/1000000:.2f} lakhs")
    print(f"Avoided Fraud: ₹{float(avoided_fraud)/10000000:.1f} crores")
    print(f"ROI Multiple: {float(roi_multiple):.1f}x")
    print(f"Savings: {float(roi_multiple):.1f} times the engagement cost")


def demo_database_schema():
    """Demonstrate database schema information"""
    print("=== Database Schema Demo ===")
    
    populator = DatabasePopulator()
    
    print("Tables that would be created:")
    print("1. employees - Employee information")
    print("2. security_metrics - Click rates and reporting statistics")
    print("3. usb_incidents - USB device usage incidents")
    print("4. intrusion_attempts - Network intrusion attempts")
    print("5. roi_tracking - Return on investment calculations")
    
    print("\nSample MySQL employees table SQL:")
    populator.db_type = 'mysql'
    sql = populator._get_employees_table_sql()
    print(sql[:200] + "..." if len(sql) > 200 else sql)
    
    print("\nSample PostgreSQL employees table SQL:")
    populator.db_type = 'postgresql'
    sql = populator._get_employees_table_sql()
    print(sql[:200] + "..." if len(sql) > 200 else sql)


def demo_user_interaction():
    """Demonstrate typical user interaction flow"""
    print("=== User Interaction Flow Demo ===")
    
    print("Typical script flow:")
    print("1. User enters database connection details")
    print("   - Database type: mysql or postgresql")
    print("   - Host: localhost (default)")
    print("   - Port: 3306 (MySQL) or 5432 (PostgreSQL)")
    print("   - Database name, username, password")
    
    print("\n2. Script creates tables if they don't exist")
    print("   - All 5 tables created successfully")
    
    print("\n3. Script checks for existing data")
    print("   - If data exists: prompts to delete")
    print("   - If no data: proceeds to generation")
    
    print("\n4. User specifies number of employees")
    print("   - Script generates all related data")
    print("   - Displays statistics summary")


def main():
    """Run all demos"""
    print("FISST Academy Database Populator - Demo")
    print("=" * 50)
    
    demo_user_interaction()
    print("\n" + "=" * 50)
    
    demo_database_schema()
    print("\n" + "=" * 50)
    
    demo_indian_data_generation()
    print("=" * 50)
    
    demo_security_metrics()
    print("\n" + "=" * 50)
    
    demo_roi_calculation()
    print("\n" + "=" * 50)
    
    print("Demo completed! The actual script can be run with:")
    print("python database_populator.py")
    print("\nNote: Actual database connection required for full functionality.")


if __name__ == "__main__":
    main()