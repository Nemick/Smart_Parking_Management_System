"""
Smart Parking System - Quick Start Guide
Run this file to verify everything is set up correctly
"""

import sys
import subprocess

def check_imports():
    """Check if all required packages are installed"""
    packages = {
        'streamlit': 'Streamlit (Web Framework)',
        'pandas': 'Pandas (Data Processing)',
        'plotly': 'Plotly (Visualizations)',
        'cv2': 'OpenCV (Image Processing)',
        'easyocr': 'EasyOCR (Text Recognition)',
        'ultralytics': 'YOLOv8 (Detection Model)',
        'torch': 'PyTorch (Deep Learning)',
        'PIL': 'Pillow (Image Library)'
    }
    
    print("\n" + "="*60)
    print("CHECKING DEPENDENCIES")
    print("="*60 + "\n")
    
    missing = []
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"✅ {name:<40} OK")
        except ImportError:
            print(f"❌ {name:<40} MISSING")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️ Missing packages: {', '.join(missing)}")
        print("\nRun: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed!")
    return True

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'parking_system.py',
        'read_plate_number.py',
        'test.py',
        'trained_license_plate_detector.pt',
        'requirements.txt'
    ]
    
    print("\n" + "="*60)
    print("CHECKING FILES")
    print("="*60 + "\n")
    
    import os
    missing = []
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / (1024*1024)  # MB
            print(f"✅ {file:<40} ({size:.2f} MB)")
        else:
            print(f"❌ {file:<40} MISSING")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️ Missing files: {', '.join(missing)}")
        return False
    
    print("\n✅ All required files present!")
    return True

def run_streamlit():
    """Run the Streamlit app"""
    print("\n" + "="*60)
    print("STARTING STREAMLIT APPLICATION")
    print("="*60 + "\n")
    print("Opening browser at: http://localhost:8501")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run(["streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n\nStreamlit stopped.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Check dependencies
    if not check_imports():
        print("\n❌ Please install missing dependencies first!")
        sys.exit(1)
    
    # Check files
    if not check_files():
        print("\n❌ Please ensure all files are present!")
        sys.exit(1)
    
    # All checks passed
    print("\n" + "="*60)
    print("✅ SYSTEM READY - ALL CHECKS PASSED!")
    print("="*60)
    
    # Ask to run
    response = input("\nStart Streamlit app? (y/n): ").strip().lower()
    if response == 'y':
        run_streamlit()
    else:
        print("\nTo start the app later, run: streamlit run app.py")
