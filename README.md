# Python Database Populator

A Python script that populates databases with realistic fake data for the FISST Academy cybersecurity case study simulation.

## Features

- Supports MySQL and PostgreSQL databases
- Generates realistic Indian employee data using Faker library
- Creates security metrics data simulating cybersecurity training outcomes
- Tracks USB incidents, intrusion attempts, and ROI metrics
- Interactive command-line interface with yes/no prompts
- Data validation and existence checking
- Statistical summary aligned with case study requirements

## Requirements

- Python 3.6+
- MySQL or PostgreSQL database server
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/shadow-dragon-2002/python-database-populator.git
cd python-database-populator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python database_populator.py
```

The script will prompt you for:
1. Database type (MySQL or PostgreSQL)
2. Connection details (host, port, database name, username, password)
3. Whether to delete existing data (if any)
4. Number of employees to generate

## Database Schema

The script creates the following tables:

- **employees**: Employee information with Indian names, addresses, and contact details
- **security_metrics**: Click rates, reporting rates, and training outcomes
- **usb_incidents**: USB device usage incidents
- **intrusion_attempts**: Network intrusion attempts and blocking status
- **roi_tracking**: Return on investment calculations

## Case Study Simulation

The generated data simulates the FISST Academy cybersecurity case study outcomes:

- **Baseline metrics**: ~22% click rate, 0% reporting, 11 USB incidents
- **Post-intervention**: ~5% click rate, ~38% reporting, 0 USB incidents
- **ROI**: ₹7.3 crore avoided fraud, 15x return on investment
- **Organization**: All employees belong to "FISST Academy"

## Example Output

```
FISST Academy Database Populator
========================================
Enter database type (mysql/postgresql): mysql
Enter host (default: localhost): 
Enter port (default: 3306): 
Enter database name: fisst_academy
Enter username: root
Enter password: 

✓ Successfully connected to mysql database!
✓ Created table: employees
✓ Created table: security_metrics
✓ Created table: usb_incidents
✓ Created table: intrusion_attempts
✓ Created table: roi_tracking
✓ All tables created successfully!

Enter the number of employees to create: 50

Generating data for 50 employees...
✓ Generated 50 employees successfully!
✓ Generated 250 security metrics entries!
✓ Generated 11 USB incident entries!
✓ Generated 50 intrusion attempt entries!
✓ Generated ROI tracking entry!

✓ All data generated successfully!

=== Generated Data Statistics Summary ===
Click Rate: 22.1% (baseline) → 5.2% (post-intervention)
Reporting Rate: 0.0% (baseline) → 37.8% (post-intervention)
USB Incidents: 11 (before intervention) → 0 (after intervention)
Intrusion Attempts: 50 blocked at reception
ROI: ₹73.0 crore avoided fraud, 15x return on investment
```