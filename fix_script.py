#!/usr/bin/env python3
"""
Fix script for database populator issues
This script helps resolve common issues with the database populator
"""

import os
import sys
import subprocess
import shutil


def clear_python_cache():
    """Clear Python cache files"""
    print("🧹 Clearing Python cache files...")
    
    cache_dirs = []
    cache_files = []
    
    # Find and remove __pycache__ directories
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_path = os.path.join(root, '__pycache__')
            cache_dirs.append(cache_path)
        
        # Find .pyc files
        for file in files:
            if file.endswith('.pyc'):
                cache_files.append(os.path.join(root, file))
    
    # Remove cache directories
    for cache_dir in cache_dirs:
        try:
            shutil.rmtree(cache_dir)
            print(f"   ✓ Removed: {cache_dir}")
        except Exception as e:
            print(f"   ✗ Failed to remove {cache_dir}: {e}")
    
    # Remove .pyc files
    for cache_file in cache_files:
        try:
            os.remove(cache_file)
            print(f"   ✓ Removed: {cache_file}")
        except Exception as e:
            print(f"   ✗ Failed to remove {cache_file}: {e}")
    
    print(f"🧹 Cleared {len(cache_dirs)} cache directories and {len(cache_files)} cache files")


def verify_installation():
    """Verify the database populator installation"""
    print("\n🔍 Verifying database populator installation...")
    
    try:
        # Check if main file exists
        if not os.path.exists('database_populator.py'):
            print("   ✗ database_populator.py not found!")
            return False
        
        print("   ✓ database_populator.py found")
        
        # Check Python syntax
        try:
            import ast
            with open('database_populator.py', 'r') as f:
                source = f.read()
            ast.parse(source)
            print("   ✓ Python syntax is valid")
        except SyntaxError as e:
            print(f"   ✗ Syntax error in database_populator.py: {e}")
            return False
        
        # Try importing the module
        try:
            from database_populator import DatabasePopulator
            print("   ✓ Module imports successfully")
        except ImportError as e:
            print(f"   ✗ Import error: {e}")
            return False
        
        # Check if all required methods exist
        dp = DatabasePopulator()
        required_methods = [
            '_get_employee_master_table_sql',
            '_get_employee_phish_smish_sim_table_sql',
            '_get_employee_vishing_sim_table_sql',
            '_get_employee_quishing_sim_table_sql',
            '_get_red_team_assessment_table_sql'
        ]
        
        missing_methods = []
        for method_name in required_methods:
            if not hasattr(dp, method_name):
                missing_methods.append(method_name)
        
        if missing_methods:
            print(f"   ✗ Missing methods: {missing_methods}")
            return False
        else:
            print(f"   ✓ All {len(required_methods)} table creation methods found")
        
        # Test method calls
        dp.db_type = 'mysql'
        try:
            for method_name in required_methods:
                method = getattr(dp, method_name)
                result = method()
                if not result or 'CREATE TABLE' not in result:
                    print(f"   ✗ Method {method_name} returns invalid SQL")
                    return False
            print("   ✓ All methods return valid SQL")
        except Exception as e:
            print(f"   ✗ Error calling methods: {e}")
            return False
        
        print("   ✅ Installation verification passed!")
        return True
        
    except Exception as e:
        print(f"   ✗ Verification failed: {e}")
        return False


def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    if not os.path.exists('requirements.txt'):
        print("   ✗ requirements.txt not found!")
        return False
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--quiet'])
        print("   ✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ✗ Failed to install dependencies: {e}")
        return False


def run_demo():
    """Run the demo to verify functionality"""
    print("\n🧪 Running demo to verify functionality...")
    
    try:
        result = subprocess.run([sys.executable, 'demo_full_workflow.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            if "🎉 Demo completed successfully!" in result.stdout:
                print("   ✅ Demo ran successfully!")
                return True
            else:
                print("   ⚠️  Demo ran but didn't complete successfully")
                print(f"   Output: {result.stdout[-200:]}")  # Last 200 chars
                return False
        else:
            print(f"   ✗ Demo failed with return code {result.returncode}")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("   ✗ Demo timed out")
        return False
    except Exception as e:
        print(f"   ✗ Error running demo: {e}")
        return False


def main():
    """Main fix function"""
    print("Database Populator Fix Script")
    print("=" * 40)
    print("🔧 This script will help fix common issues with the database populator")
    print("")
    
    # Step 1: Clear cache
    clear_python_cache()
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies. Please run manually:")
        print("   pip install -r requirements.txt")
        return
    
    # Step 3: Verify installation
    if not verify_installation():
        print("\n❌ Installation verification failed!")
        print("💡 Suggestions:")
        print("   • Make sure you're in the correct directory")
        print("   • Try downloading the files again")
        print("   • Check if you have the latest version")
        return
    
    # Step 4: Run demo
    if not run_demo():
        print("\n⚠️  Demo test failed, but core verification passed")
        print("💡 You can still try running the main script manually:")
        print("   python database_populator.py")
        return
    
    print("\n🎉 All checks passed! Database populator is ready to use.")
    print("")
    print("📚 Usage options:")
    print("   python database_populator.py          # Main script (requires database)")
    print("   python demo_full_workflow.py          # Demo with SQLite (no database needed)")
    print("   python validate_script.py             # Validate functionality")
    print("   python database_populator.py --help   # Show help")
    print("")
    print("🔧 If you still have issues:")
    print("   • Check TROUBLESHOOTING.md for detailed solutions")
    print("   • Make sure your database server is running")
    print("   • Verify database connection credentials")


if __name__ == "__main__":
    main()