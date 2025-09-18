# Database Connection Troubleshooting Guide

## Common Database Connection Issues and Solutions

### 🔍 Quick Diagnosis

When you see a connection error, look for these keywords in the error message:

- **"Access denied"** → Authentication problem
- **"Can't connect"** or **"Connection refused"** → Server not reachable
- **"Unknown database"** → Database doesn't exist
- **"timeout"** → Network or server performance issue

### ❌ Access Denied Errors

**Error Examples:**
- `Access denied for user 'root'@'4.240.39.196' (using password: YES)`
- `Authentication failed`

**Solutions:**
1. **Check Username/Password**
   ```bash
   # Test connection manually
   mysql -h your_host -u your_username -p
   ```

2. **Verify User Privileges**
   ```sql
   -- Grant privileges (run as admin user)
   GRANT ALL PRIVILEGES ON *.* TO 'username'@'%' IDENTIFIED BY 'password';
   FLUSH PRIVILEGES;
   ```

3. **For Remote Connections**
   - Ensure user has remote access (`'username'@'%'` not just `'username'@'localhost'`)
   - Check MySQL bind-address in `/etc/mysql/mysql.conf.d/mysqld.cnf`

### 🔌 Connection Refused Errors

**Error Examples:**
- `Can't connect to MySQL server on 'host:3306'`
- `Connection refused`

**Solutions:**
1. **Check if Database Server is Running**
   ```bash
   # For MySQL
   sudo systemctl status mysql
   sudo systemctl start mysql
   
   # For PostgreSQL
   sudo systemctl status postgresql
   sudo systemctl start postgresql
   ```

2. **Verify Host and Port**
   - Use `localhost` or `127.0.0.1` for local connections
   - Default ports: MySQL=3306, PostgreSQL=5432

3. **Check Firewall Settings**
   ```bash
   # Allow MySQL port
   sudo ufw allow 3306
   
   # Allow PostgreSQL port
   sudo ufw allow 5432
   ```

### 📂 Database Not Found Errors

**Error Examples:**
- `Unknown database 'database_name'`
- `database "database_name" does not exist`

**Solutions:**
1. **Create the Database**
   ```sql
   -- MySQL
   CREATE DATABASE your_database_name;
   
   -- PostgreSQL
   CREATE DATABASE your_database_name;
   ```

2. **List Existing Databases**
   ```sql
   -- MySQL
   SHOW DATABASES;
   
   -- PostgreSQL
   \l
   ```

### ⏱️ Timeout Errors

**Error Examples:**
- `Connection timeout`
- `Lost connection to MySQL server`

**Solutions:**
1. **Check Network Connectivity**
   ```bash
   ping your_database_host
   telnet your_database_host 3306
   ```

2. **Increase Timeout Values**
   - The script now uses 10-second timeout by default
   - Check if server is overloaded

### 🔧 Quick Setup for Local Testing

#### MySQL Local Setup
```bash
# Install MySQL
sudo apt update
sudo apt install mysql-server

# Start MySQL
sudo systemctl start mysql

# Secure installation (optional)
sudo mysql_secure_installation

# Create database and user
sudo mysql -e "CREATE DATABASE fisst_academy;"
sudo mysql -e "CREATE USER 'fisst_user'@'localhost' IDENTIFIED BY 'secure_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON fisst_academy.* TO 'fisst_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

#### PostgreSQL Local Setup
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql

# Create database and user
sudo -u postgres createdb fisst_academy
sudo -u postgres createuser --interactive fisst_user
sudo -u postgres psql -c "ALTER USER fisst_user PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE fisst_academy TO fisst_user;"
```

### 🧪 Testing Without Database Setup

If you want to test the script functionality without setting up a database:

```bash
# Run the demo with SQLite (no setup needed)
python demo_full_workflow.py

# Validate script functionality
python validate_script.py

# Get help
python database_populator.py --help
```

### 🚨 Emergency Solutions

If nothing else works:

1. **Use SQLite Demo Mode**
   ```bash
   python demo_full_workflow.py
   ```

2. **Check Error Logs**
   ```bash
   # MySQL logs
   sudo tail -f /var/log/mysql/error.log
   
   # PostgreSQL logs
   sudo tail -f /var/log/postgresql/postgresql-*.log
   ```

3. **Reset Database User**
   ```sql
   -- MySQL (as root)
   DROP USER IF EXISTS 'your_user'@'localhost';
   CREATE USER 'your_user'@'localhost' IDENTIFIED BY 'new_password';
   GRANT ALL PRIVILEGES ON *.* TO 'your_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### 📞 Getting Help

If you continue to have issues:

1. Run the script with `--help` flag for usage information
2. Check the error message carefully - it now provides specific troubleshooting steps
3. Try the demo mode first to ensure the script logic works
4. Verify your database server is accessible using command-line tools
5. Check database server logs for additional error details

The enhanced error handling in the script now provides context-specific troubleshooting information when connection failures occur.