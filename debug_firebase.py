#!/usr/bin/env python3
"""
Firebase Debug Script
This script helps debug Firebase authentication issues
"""

import sys
import os
import django

# Add the project directory to Python path
sys.path.append('/workspace/project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from app.firebase import db, auth_instance

def test_firebase_connection():
    """Test basic Firebase connectivity"""
    print("🔥 Testing Firebase Connection...")
    
    try:
        # Test database connection
        print("📊 Testing database connection...")
        test_data = db.child("test").get()
        print(f"✅ Database connection successful")
        
        # Test admin node
        print("👑 Checking admin node...")
        admin_users = db.child("admin").get()
        if admin_users.val():
            print(f"📋 Admin users found: {admin_users.val()}")
        else:
            print("⚠️ No admin users found or admin node is empty")
        
        # Test userRegistrations node
        print("👥 Checking userRegistrations node...")
        user_registrations = db.child("userRegistrations").get()
        if user_registrations.val():
            print(f"📋 User registrations found: {user_registrations.val()}")
        else:
            print("⚠️ No user registrations found or userRegistrations node is empty")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    return True

def test_firebase_auth(email, password):
    """Test Firebase authentication with specific credentials"""
    print(f"\n🔐 Testing Firebase Authentication for: {email}")
    
    try:
        # Attempt authentication
        user = auth_instance.sign_in_with_email_and_password(email, password)
        print(f"✅ Authentication successful!")
        print(f"📝 User data: {user}")
        return True
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print(f"🔍 Error type: {type(e)}")
        print(f"📋 Error details: {repr(e)}")
        return False

def find_user_in_database(email):
    """Find user in both admin and userRegistrations nodes"""
    print(f"\n🔍 Searching for user: {email}")
    
    # Check admin node
    try:
        admin_users = db.child("admin").get()
        if admin_users.each():
            for a in admin_users.each():
                if a.val().get("email") == email:
                    print(f"✅ Found in admin node: {a.val()}")
                    return 'admin', a.val()
    except Exception as e:
        print(f"❌ Error checking admin node: {e}")
    
    # Check userRegistrations node
    try:
        all_users = db.child("userRegistrations").get()
        if all_users.each():
            for u in all_users.each():
                if u.val().get("email") == email:
                    print(f"✅ Found in userRegistrations node: {u.val()}")
                    return 'user', u.val()
    except Exception as e:
        print(f"❌ Error checking userRegistrations node: {e}")
    
    print(f"❌ User not found in database")
    return None, None

def main():
    print("🚀 Firebase Debug Tool")
    print("=" * 50)
    
    # Test basic connection
    if not test_firebase_connection():
        print("❌ Basic Firebase connection failed. Check your configuration.")
        return
    
    # Get test credentials from user
    print("\n" + "=" * 50)
    email = input("Enter email to test: ").strip()
    password = input("Enter password to test: ").strip()
    
    if not email or not password:
        print("❌ Email and password are required")
        return
    
    # Test authentication
    auth_success = test_firebase_auth(email, password)
    
    # Search for user in database
    user_role, user_data = find_user_in_database(email)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"🔐 Firebase Auth: {'✅ SUCCESS' if auth_success else '❌ FAILED'}")
    print(f"📊 Database User: {'✅ FOUND' if user_data else '❌ NOT FOUND'}")
    if user_role:
        print(f"👤 User Role: {user_role}")
        print(f"📋 User Status: {user_data.get('status', 'N/A')}")
    
    if not auth_success:
        print("\n🔧 TROUBLESHOOTING TIPS:")
        print("1. Check if the email/password is correct")
        print("2. Verify Firebase Authentication is enabled")
        print("3. Check Firebase project configuration")
        print("4. Ensure the user exists in Firebase Auth")
    
    if not user_data:
        print("\n🔧 DATABASE TIPS:")
        print("1. Check if the user exists in admin or userRegistrations node")
        print("2. Verify Firebase Database rules allow read access")
        print("3. Check the database structure")

if __name__ == "__main__":
    main()