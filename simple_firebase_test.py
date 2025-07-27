#!/usr/bin/env python3
"""
Simple Firebase Test Script
Tests Firebase authentication without Django dependencies
"""

import pyrebase

# Firebase configuration - you'll need to update this with your actual config
firebase_config = {
    "apiKey": "your-api-key",
    "authDomain": "your-project.firebaseapp.com",
    "databaseURL": "https://your-project-default-rtdb.firebaseio.com/",
    "projectId": "your-project-id",
    "storageBucket": "your-project.appspot.com",
    "messagingSenderId": "your-sender-id",
    "appId": "your-app-id"
}

def test_firebase_basic():
    """Test basic Firebase setup"""
    try:
        firebase = pyrebase.initialize_app(firebase_config)
        auth = firebase.auth()
        db = firebase.database()
        print("✅ Firebase initialized successfully")
        return auth, db
    except Exception as e:
        print(f"❌ Firebase initialization failed: {e}")
        return None, None

def test_authentication(auth, email, password):
    """Test Firebase authentication"""
    print(f"\n🔐 Testing authentication for: {email}")
    
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print("✅ Authentication successful!")
        print(f"📝 User ID: {user.get('localId', 'N/A')}")
        print(f"📧 Email: {user.get('email', 'N/A')}")
        return True, user
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print(f"🔍 Error type: {type(e).__name__}")
        return False, None

def test_database_access(db, email):
    """Test database access and user lookup"""
    print(f"\n📊 Testing database access for: {email}")
    
    try:
        # Test admin node
        print("👑 Checking admin node...")
        admin_data = db.child("admin").get()
        admin_found = False
        
        if admin_data.val():
            for key, value in admin_data.val().items():
                if value.get("email") == email:
                    print(f"✅ Found in admin: {value}")
                    admin_found = True
                    break
        
        if not admin_found:
            print("ℹ️ Not found in admin node")
        
        # Test userRegistrations node
        print("👥 Checking userRegistrations node...")
        users_data = db.child("userRegistrations").get()
        user_found = False
        
        if users_data.val():
            for key, value in users_data.val().items():
                if value.get("email") == email:
                    print(f"✅ Found in userRegistrations: {value}")
                    user_found = True
                    break
        
        if not user_found:
            print("ℹ️ Not found in userRegistrations node")
        
        return admin_found or user_found
        
    except Exception as e:
        print(f"❌ Database access failed: {e}")
        return False

def main():
    print("🚀 Simple Firebase Test")
    print("=" * 50)
    
    # Initialize Firebase
    auth, db = test_firebase_basic()
    if not auth or not db:
        print("Please update the firebase_config in this script with your actual Firebase configuration.")
        return
    
    # Get test credentials
    email = input("\nEnter email to test: ").strip()
    password = input("Enter password to test: ").strip()
    
    if not email or not password:
        print("❌ Email and password are required")
        return
    
    # Test authentication
    auth_success, user_data = test_authentication(auth, email, password)
    
    # Test database access
    db_success = test_database_access(db, email)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"🔐 Authentication: {'✅ SUCCESS' if auth_success else '❌ FAILED'}")
    print(f"📊 Database Lookup: {'✅ FOUND' if db_success else '❌ NOT FOUND'}")
    
    if not auth_success:
        print("\n🔧 AUTHENTICATION TROUBLESHOOTING:")
        print("1. Verify the email and password are correct")
        print("2. Check if the user exists in Firebase Authentication")
        print("3. Ensure Firebase Authentication is enabled in your project")
        print("4. Verify your Firebase configuration is correct")
    
    if not db_success:
        print("\n🔧 DATABASE TROUBLESHOOTING:")
        print("1. Check if the user exists in admin or userRegistrations node")
        print("2. Verify Firebase Database rules allow read access")
        print("3. Check your database structure")

if __name__ == "__main__":
    main()