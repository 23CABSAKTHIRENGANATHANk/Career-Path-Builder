import sys
import os

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

print("\nChecking imports...")
try:
    import PyPDF2
    print(f"✅ PyPDF2 imported successfully (Version: {PyPDF2.__version__})")
except ImportError as e:
    print(f"❌ Failed to import PyPDF2: {e}")

try:
    import docx
    print(f"✅ python-docx imported successfully")
except ImportError as e:
    print(f"❌ Failed to import docx (python-docx): {e}")

try:
    import numpy
    print(f"✅ numpy imported successfully (Version: {numpy.__version__})")
except ImportError as e:
    print(f"❌ Failed to import numpy: {e}")

print("\nChecking uploads directory...")
upload_dir = os.path.join(os.path.dirname(__file__), 'backend', 'uploads')
print(f"Uploads path: {upload_dir}")

if not os.path.exists(upload_dir):
    try:
        os.makedirs(upload_dir)
        print(f"✅ Created uploads directory")
    except Exception as e:
        print(f"❌ Failed to create uploads directory: {e}")
else:
    print(f"✅ Uploads directory exists")

if os.path.exists(upload_dir):
    test_file = os.path.join(upload_dir, 'test_write.txt')
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        print(f"✅ Successfully wrote to uploads directory")
        os.remove(test_file)
        print(f"✅ Successfully deleted test file")
    except Exception as e:
        print(f"❌ Failed to write to uploads directory: {e}")
