# Data Generation Distribution Changes

## Overview
This document describes the changes made to ensure even distribution of simulation types and testing statuses in the database populator.

## Problem Statement
The original implementation used `random.choice()` to select simulation types and testing statuses, which could lead to:
1. Uneven distribution across categories
2. Lack of alignment between simulation types and test types
3. Potential bias towards certain values

## Solution
Implemented round-robin (cyclic) selection for all categorical fields to ensure even distribution.

## Changes Made

### 1. Employee Master Table (`generate_employees`)
**Simulation Type Field:**
- **Before:** `simulation_type = 'Baseline Assessment'` (hardcoded)
- **After:** Cycles through `['Phishing Test', 'Vishing Test', 'Quishing Test', 'Red Team Assessment']`
- **Alignment:** Now explicitly reflects the test type being conducted

**Testing Status Fields:**
- **phish_testing_status:** Even distribution across `['Completed', 'Pending', 'Failed', 'Passed']`
- **vish_testing_status:** Even distribution across `['Completed', 'Pending', 'Failed', 'Passed']`
- **red_team_testing_status:** Even distribution across `['Completed', 'In Progress', 'Scheduled', 'Cancelled']`

### 2. Phishing/Smishing Simulations (`generate_phish_smish_simulations`)
**Simulation Type:**
- **Before:** `random.choice(['Email Phishing', 'SMS Phishing', 'Social Media Phishing'])`
- **After:** Round-robin selection through the list
- **Result:** Each type gets approximately 33.3% of records

**Testing Status:**
- **Before:** `random.choice(['Completed', 'Pending', 'Failed', 'Passed'])`
- **After:** Round-robin selection through the list
- **Result:** Each status gets approximately 25% of records

### 3. Vishing Simulations (`generate_vishing_simulations`)
**Testing Status:**
- **Before:** `random.choice(['Completed', 'Pending', 'Failed', 'Passed'])`
- **After:** Round-robin selection through the list
- **Result:** Each status gets approximately 25% of records

### 4. Quishing Simulations (`generate_quishing_simulations`)
**Multiple Fields with Even Distribution:**
- **qr_code_type:** Round-robin through 6 QR code types (~16.7% each)
- **device_type:** Round-robin through 4 device types (25% each)
- **testing_status:** Round-robin through 4 statuses (25% each)
- **malicious_qr_clicked:** Alternates True/False (50% each)

### 5. Red Team Assessments (`generate_red_team_assessments`)
**Testing Status:**
- **Before:** `random.choice(['Completed', 'In Progress', 'Scheduled', 'Cancelled'])`
- **After:** Round-robin selection through the list
- **Result:** Each status gets approximately 25% of records

## Implementation Details

### Round-Robin Pattern
```python
# Index counter for even distribution
status_idx = 0

for record in records:
    # Select value using modulo operator for cycling
    status = statuses[status_idx % len(statuses)]
    status_idx += 1
```

### Benefits
1. **Predictable Distribution:** Each category receives equal representation
2. **No Bias:** Eliminates random clustering of values
3. **Alignment:** Simulation types now explicitly reflect test types
4. **Consistency:** Works reliably regardless of dataset size

## Testing

### New Tests Added
- `test_distribution.py`: Comprehensive test suite validating:
  - Simulation type alignment with test types
  - Even distribution of all simulation types
  - Even distribution of all testing statuses
  - Multiple scenarios with different dataset sizes

### Demo Script
- `demo_distribution.py`: Demonstrates the even distribution with sample outputs

### Validation Results
```
For 100 records with 4 categories:
  Category 1: 25 records (25%)
  Category 2: 25 records (25%)
  Category 3: 25 records (25%)
  Category 4: 25 records (25%)
```

## Examples

### Before (Random Selection)
```
Simulation Type Distribution (100 records):
  Email Phishing: 28 (28%)      # Uneven
  SMS Phishing: 41 (41%)        # Uneven
  Social Media Phishing: 31 (31%)  # Uneven
```

### After (Round-Robin)
```
Simulation Type Distribution (100 records):
  Email Phishing: 34 (34%)      # Even (~33.3%)
  SMS Phishing: 33 (33%)        # Even (~33.3%)
  Social Media Phishing: 33 (33%)  # Even (~33.3%)
```

## Compatibility
- No breaking changes to database schema
- No changes to API or method signatures
- All existing tests pass
- Backward compatible with existing workflows

## Files Modified
1. `database_populator.py` - Core data generation logic
2. `test_distribution.py` - New test suite (added)
3. `demo_distribution.py` - New demo script (added)

## Verification
Run the following to verify changes:
```bash
# Run distribution tests
python test_distribution.py

# Run demo
python demo_distribution.py

# Run existing tests
python test_database_populator.py
python test_consistency.py
```

## Future Considerations
- Consider adding configuration options for custom distribution patterns
- Could extend to support weighted distributions if needed
- May add reporting tools to analyze distribution in actual database records
