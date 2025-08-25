#!/usr/bin/env python3
"""
Setup script for Zomato-like App
This script initializes the database and runs migrations
"""

import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    try:
        logger.info(f"Running {description}...")
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        logger.info(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {description} failed:")
        logger.error(f"Error: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.error(f"❌ Script {script_name} not found")
        return False

def main():
    """Main setup function"""
    logger.info("🚀 Starting Zomato-like App setup...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        logger.warning("⚠️  .env file not found. Creating default .env file...")
        with open('.env', 'w') as f:
            f.write("""# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
DB_NAME=zomato

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
""")
        logger.info("✅ Created default .env file")
    
    # Initialize database
    if not run_script('init_db.py', 'Database initialization'):
        logger.error("❌ Setup failed at database initialization")
        return False
    
    # Run database migration
    if not run_script('migrate_db.py', 'Database migration'):
        logger.error("❌ Setup failed at database migration")
        return False
    
    logger.info("🎉 Setup completed successfully!")
    logger.info("📝 Next steps:")
    logger.info("   1. Update .env file with your database credentials")
    logger.info("   2. Install dependencies: pip install -r requirements.txt")
    logger.info("   3. Run the app: python app.py")
    logger.info("   4. Access the app at: http://localhost:5000")
    logger.info("   5. Login with demo credentials: alice/password123")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
