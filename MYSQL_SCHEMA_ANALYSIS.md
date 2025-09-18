# MySQL Database Schema Analysis and Implementation

## Extracted Database Schema

Based on the provided SQL commands, here are the exact table names and column specifications:

### 1. Table: `employee_master`
**Primary Keys:** `serial_no` (AUTO_INCREMENT), `employee_id` (UNIQUE)

**Columns:**
- `serial_no` INT AUTO_INCREMENT PRIMARY KEY
- `employee_id` INT UNIQUE
- `first_name` VARCHAR(50)
- `last_name` VARCHAR(50)
- `gender` CHAR(1)
- `date_of_birth` DATE
- `age` INT
- `blood_group` VARCHAR(5)
- `marital_status` VARCHAR(20)
- `email` VARCHAR(100)
- `phone_number` VARCHAR(20)
- `address` VARCHAR(255)
- `state` VARCHAR(50)
- `postal_code` VARCHAR(10)
- `country` VARCHAR(50)
- `designation` VARCHAR(50)
- `department` VARCHAR(50)
- `salary` DECIMAL(10,2)
- `work_experience_years` DECIMAL(4,1)
- `joining_date` DATE
- `emergency_contact_name` VARCHAR(100)
- `emergency_contact_phone` VARCHAR(20)
- `family_details` VARCHAR(255)
- `medical_conditions` VARCHAR(255)
- `simulation_type` VARCHAR(50)
- `work_email` VARCHAR(100)
- `personal_email` VARCHAR(100)

**Phishing/Smishing Fields:**
- `click_response_rate` DECIMAL(5,2)
- `phish_last_simulation_date` DATE
- `phish_testing_status` VARCHAR(20)

**Vishing Fields:**
- `vishing_phone_number` VARCHAR(20)
- `vishing_alt_phone_number` VARCHAR(20)
- `voice_auth_test` BOOLEAN
- `vish_response_rate` DECIMAL(5,2)
- `vish_last_simulation_date` DATE
- `vish_testing_status` VARCHAR(20)

**Quishing Fields:**
- `quish_response_rate` DECIMAL(5,2)
- `quish_last_simulation_date` DATE
- `quish_testing_status` VARCHAR(20)

**Red Team Assessment Fields:**
- `branch_location` VARCHAR(100)
- `branch_code` VARCHAR(10)
- `total_employees_at_branch` INT
- `security_level` VARCHAR(20)
- `building_storeys` INT
- `assessment_date` DATE
- `assessment_time_start` TIME
- `assessment_time_end` TIME
- `permission_granted` BOOLEAN
- `approving_official_name` VARCHAR(100)
- `approving_official_designation` VARCHAR(100)
- `identity_verification_required` BOOLEAN
- `identity_verified` BOOLEAN
- `security_guard_present` BOOLEAN
- `visitor_log_maintained` BOOLEAN
- `badge_issued` BOOLEAN
- `escort_required` BOOLEAN
- `restricted_areas_accessed` BOOLEAN
- `tailgating_possible` BOOLEAN
- `social_engineering_successful` BOOLEAN
- `physical_security_score` DECIMAL(3,1)
- `human_security_score` DECIMAL(3,1)
- `overall_assessment_score` DECIMAL(3,1)
- `vulnerabilities_found` VARCHAR(255)
- `recommendations` VARCHAR(255)
- `assessor_name` VARCHAR(100)
- `assessor_id` VARCHAR(20)
- `notes` VARCHAR(255)
- `red_team_testing_status` VARCHAR(20)
- `organisation_name` VARCHAR(100)

### 2. Table: `employee_phish_smish_sim`
**Primary Key:** `sim_id` (AUTO_INCREMENT)
**Foreign Keys:** `serial_no` → `employee_master(serial_no)`, `employee_id` → `employee_master(employee_id)`

**Columns:**
- `sim_id` INT AUTO_INCREMENT PRIMARY KEY
- `serial_no` INT
- `employee_id` INT
- `simulation_type` VARCHAR(20)
- `work_email` VARCHAR(100)
- `personal_email` VARCHAR(100)
- `phone_number` VARCHAR(20)
- `click_response_rate` DECIMAL(5,2)
- `last_simulation_date` DATE
- `testing_status` VARCHAR(20)

### 3. Table: `employee_vishing_sim`
**Primary Key:** `vish_id` (AUTO_INCREMENT)
**Foreign Keys:** `serial_no` → `employee_master(serial_no)`, `employee_id` → `employee_master(employee_id)`

**Columns:**
- `vish_id` INT AUTO_INCREMENT PRIMARY KEY
- `serial_no` INT
- `employee_id` INT
- `phone_number` VARCHAR(20)
- `alt_phone_number` VARCHAR(20)
- `voice_auth_test` BOOLEAN
- `vish_response_rate` DECIMAL(5,2)
- `last_simulation` DATE
- `testing_status` VARCHAR(20)

### 4. Table: `employee_quishing_sim`
**Primary Key:** `quish_id` (AUTO_INCREMENT)
**Foreign Keys:** `serial_no` → `employee_master(serial_no)`, `employee_id` → `employee_master(employee_id)`

**Columns:**
- `quish_id` INT AUTO_INCREMENT PRIMARY KEY
- `serial_no` INT
- `employee_id` INT
- `qr_code_link` VARCHAR(255)
- `device_used` VARCHAR(50)
- `scan_location` VARCHAR(100)
- `scan_time` TIMESTAMP
- `response_action` VARCHAR(50)
- `quish_response_rate` DECIMAL(5,2)
- `last_simulation_date` DATE
- `testing_status` VARCHAR(20)

### 5. Table: `red_team_assessment`
**Primary Key:** `assess_id` (AUTO_INCREMENT)
**Foreign Keys:** `serial_no` → `employee_master(serial_no)`, `employee_id` → `employee_master(employee_id)`

**Columns:**
- `assess_id` INT AUTO_INCREMENT PRIMARY KEY
- `serial_no` INT
- `employee_id` INT
- `branch_location` VARCHAR(100)
- `branch_code` VARCHAR(10)
- `total_employees_at_branch` INT
- `security_level` VARCHAR(20)
- `building_storeys` INT
- `assessment_date` DATE
- `assessment_time_start` TIME
- `assessment_time_end` TIME
- `permission_granted` BOOLEAN
- `approving_official_name` VARCHAR(100)
- `approving_official_designation` VARCHAR(100)
- `identity_verification_required` BOOLEAN
- `identity_verified` BOOLEAN
- `security_guard_present` BOOLEAN
- `visitor_log_maintained` BOOLEAN
- `badge_issued` BOOLEAN
- `escort_required` BOOLEAN
- `restricted_areas_accessed` BOOLEAN
- `tailgating_possible` BOOLEAN
- `social_engineering_successful` BOOLEAN
- `physical_security_score` DECIMAL(3,1)
- `human_security_score` DECIMAL(3,1)
- `overall_assessment_score` DECIMAL(3,1)
- `vulnerabilities_found` VARCHAR(255)
- `recommendations` VARCHAR(255)
- `assessor_name` VARCHAR(100)
- `assessor_id` VARCHAR(20)
- `notes` VARCHAR(255)
- `testing_status` VARCHAR(20)

## Key Changes Implemented

### 1. **MySQL-Only Implementation**
- Removed PostgreSQL support
- Uses `mysql.connector` exclusively
- Simplified database type handling

### 2. **Schema Compliance**
- `employee_id` changed from VARCHAR(20) to INT
- Updated all column names to match exact schema
- Proper foreign key relationships with both `serial_no` and `employee_id`

### 3. **No Table Creation**
- Script only populates existing tables
- Verifies all required tables exist before proceeding
- Provides clear error messages if tables are missing

### 4. **Consistent Statistics**
- Uses fixed seed (42) for reproducible results
- Same percentage rates regardless of employee count:
  - Phishing: ~23.1%
  - Vishing: ~23.6%
  - Quishing: ~23.1%
  - Physical Security: ~6.4/10
  - Human Security: ~8.9/10

### 5. **Enhanced Data Generation**
- Generates realistic Indian names, addresses, phone numbers
- Proper data types and ranges
- Complete population of all columns
- No null/empty values

## Usage

1. **Prerequisites:**
   - MySQL server running
   - All 5 tables created using provided schema
   - Python dependencies: `mysql-connector-python`, `faker`

2. **Running the Script:**
   ```bash
   python mysql_database_populator.py
   ```

3. **Features:**
   - Interactive database connection setup
   - Data existence checking with deletion option
   - Consistent statistics generation
   - Comprehensive error handling
   - Detailed progress reporting

## Statistics Consistency

The script ensures that regardless of whether you generate data for 10 employees or 1000 employees, the overall statistics will remain approximately the same:

- **Phishing Click Rate:** 23.1% ± 1%
- **Vishing Response Rate:** 23.6% ± 1%
- **Quishing Scan Rate:** 23.1% ± 1%
- **Physical Security Score:** 6.4/10 ± 0.5
- **Human Security Score:** 8.9/10 ± 0.5

This ensures reliable reporting metrics for management regardless of dataset size.