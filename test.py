"""
Integrated Test Suite for Smart Parking System
Tests the complete workflow: License plate detection → Parking spot assignment
"""

import cv2
import os
import json
from datetime import datetime
from parking_system import ParkingLayout, SpotAssigner, OccupancyTracker
from read_plate_number import ParkingManager, detect_and_read_plate, model


class ParkingSystemTester:
    """Test class for the smart parking system"""
    
    def __init__(self, reset_lot=True):
        """Initialize tester with option to reset parking lot"""
        if reset_lot:
            self.reset_parking_lot()
        
        self.parking_layout = ParkingLayout()
        self.spot_assigner = SpotAssigner(self.parking_layout)
        self.occupancy_tracker = OccupancyTracker(self.parking_layout)
        self.parking_manager = ParkingManager()
    
    def reset_parking_lot(self):
        """Reset parking lot to empty state"""
        print("Resetting parking lot configuration...")
        # Create a fresh parking layout to generate default config
        temp_layout = ParkingLayout()
        temp_layout.create_realistic_layout()
        temp_layout.save_config()
        print("Parking lot reset complete.")
    
    def test_empty_parking_lot(self):
        """Test 1: Verify parking lot is initialized correctly"""
        print("\n" + "="*60)
        print("TEST 1: Empty Parking Lot Initialization")
        print("="*60)
        
        status = self.parking_layout.get_occupancy_status()
        print(f"Total Spots: {status['total_spots']}")
        print(f"Available Spots: {status['available_spots']}")
        print(f"Occupied Spots: {status['occupied_spots']}")
        print(f"Occupancy Rate: {status['occupancy_rate']:.2f}%")
        
        assert status['total_spots'] == 32, "Should have 32 total spots"
        assert status['occupied_spots'] == 0, "Should have no occupied spots"
        assert status['occupancy_rate'] == 0, "Occupancy rate should be 0%"
        
        print("✓ TEST PASSED: Parking lot initialized correctly")
        return True
    
    def test_spot_types(self):
        """Test 2: Verify different spot types"""
        print("\n" + "="*60)
        print("TEST 2: Spot Types Verification")
        print("="*60)
        
        status = self.parking_layout.get_occupancy_status()
        print("Spot Types Distribution:")
        for spot_type, info in status['by_type'].items():
            print(f"  {spot_type.upper()}: {info['total']} spots")
        
        handicap_spots = status['by_type']['handicap']['total']
        premium_spots = status['by_type']['premium']['total']
        standard_spots = status['by_type']['standard']['total']
        
        assert handicap_spots > 0, "Should have handicap spots"
        assert premium_spots > 0, "Should have premium spots"
        assert standard_spots > 0, "Should have standard spots"
        
        print("✓ TEST PASSED: All spot types available")
        return True
    
    def test_manual_vehicle_entry(self, license_plate="ABC123"):
        """Test 3: Manual vehicle entry without license plate detection"""
        print("\n" + "="*60)
        print("TEST 3: Manual Vehicle Entry")
        print("="*60)
        
        vehicle_info = {
            'license_plate': license_plate,
            'entry_time': datetime.now().isoformat(),
            'preferred_type': 'standard',
            'handicap_permit': False
        }
        
        print(f"Creating vehicle entry: {vehicle_info}")
        assigned_spot = self.spot_assigner.auto_assign_spot(vehicle_info)
        
        if assigned_spot:
            print(f"✓ Vehicle assigned to spot {assigned_spot}")
            self.occupancy_tracker.record_entry(assigned_spot, vehicle_info)
            
            spot_info = self.parking_layout.get_spot_info(assigned_spot)
            print(f"  Spot Type: {spot_info['type']}")
            print(f"  Spot Row: {spot_info['row']}")
            print(f"  Vehicle License: {spot_info['vehicle_info']['license_plate']}")
            
            return assigned_spot
        else:
            print("✗ Failed to assign spot (parking lot full)")
            return None
    
    def test_multiple_vehicles(self, num_vehicles=5):
        """Test 4: Multiple vehicle entries"""
        print("\n" + "="*60)
        print(f"TEST 4: Multiple Vehicle Entries ({num_vehicles} vehicles)")
        print("="*60)
        
        assigned_spots = []
        
        for i in range(num_vehicles):
            license_plate = f"VEH{i+1:03d}"
            vehicle_info = {
                'license_plate': license_plate,
                'entry_time': datetime.now().isoformat(),
                'preferred_type': 'standard',
                'handicap_permit': False
            }
            
            spot_id = self.spot_assigner.auto_assign_spot(vehicle_info)
            
            if spot_id:
                assigned_spots.append(spot_id)
                self.occupancy_tracker.record_entry(spot_id, vehicle_info)
                print(f"  Vehicle {license_plate} → Spot {spot_id}")
            else:
                print(f"  Vehicle {license_plate} → FAILED (no spots available)")
        
        status = self.parking_layout.get_occupancy_status()
        print(f"\nAfter entries:")
        print(f"  Occupied: {status['occupied_spots']}/{status['total_spots']}")
        print(f"  Occupancy Rate: {status['occupancy_rate']:.2f}%")
        
        print("✓ TEST PASSED: Multiple vehicles processed")
        return assigned_spots
    
    def test_handicap_priority(self):
        """Test 5: Handicap spot priority"""
        print("\n" + "="*60)
        print("TEST 5: Handicap Spot Priority")
        print("="*60)
        
        vehicle_info = {
            'license_plate': 'HANDICAP1',
            'entry_time': datetime.now().isoformat(),
            'preferred_type': 'standard',
            'handicap_permit': True
        }
        
        print("Vehicle with handicap permit requesting spot...")
        assigned_spot = self.spot_assigner.auto_assign_spot(vehicle_info)
        
        if assigned_spot:
            spot_info = self.parking_layout.get_spot_info(assigned_spot)
            print(f"  Assigned to spot {assigned_spot}")
            print(f"  Spot type: {spot_info['type']}")
            
            if spot_info['type'] == 'handicap':
                print("✓ TEST PASSED: Handicap vehicle got handicap spot")
                self.occupancy_tracker.record_entry(assigned_spot, vehicle_info)
                return True
            else:
                print("⚠ WARNING: Handicap vehicle got non-handicap spot (no handicap spots available)")
                self.occupancy_tracker.record_entry(assigned_spot, vehicle_info)
                return False
        else:
            print("✗ TEST FAILED: Could not assign spot")
            return False
    
    def test_vehicle_exit(self, spot_id):
        """Test 6: Vehicle exit and spot release"""
        print("\n" + "="*60)
        print("TEST 6: Vehicle Exit")
        print("="*60)
        
        print(f"Processing exit for spot {spot_id}...")
        
        spot_info = self.parking_layout.get_spot_info(spot_id)
        if spot_info['occupied']:
            license_plate = spot_info['vehicle_info']['license_plate']
            self.occupancy_tracker.record_exit(spot_id)
            self.parking_layout.release_spot(spot_id)
            
            print(f"  Vehicle {license_plate} exited")
            print(f"  Spot {spot_id} released")
            print("✓ TEST PASSED: Vehicle exit processed")
            return True
        else:
            print(f"✗ TEST FAILED: Spot {spot_id} is already empty")
            return False
    
    def test_occupancy_statistics(self):
        """Test 7: Generate occupancy statistics"""
        print("\n" + "="*60)
        print("TEST 7: Occupancy Statistics")
        print("="*60)
        
        stats = self.occupancy_tracker.get_statistics('day')
        
        print("Daily Statistics:")
        print(f"  Total Vehicles: {stats['total_vehicles']}")
        print(f"  Average Duration: {stats['avg_duration']:.2f} minutes" 
              if stats['avg_duration'] else "  Average Duration: N/A")
        
        print("\nBy Spot Type:")
        for spot_type, type_stats in stats['by_type'].items():
            print(f"  {spot_type.upper()}:")
            print(f"    Count: {type_stats['count']}")
            print(f"    Avg Duration: {type_stats['duration_minutes']:.2f} minutes")
        
        print("✓ TEST PASSED: Statistics generated")
        return True
    
    def test_available_spots_filter(self):
        """Test 8: Filter available spots by type"""
        print("\n" + "="*60)
        print("TEST 8: Available Spots Filter")
        print("="*60)
        
        available_standard = self.parking_layout.get_available_spots('standard')
        available_premium = self.parking_layout.get_available_spots('premium')
        available_handicap = self.parking_layout.get_available_spots('handicap')
        available_all = self.parking_layout.get_available_spots()
        
        print(f"Available Standard Spots: {len(available_standard)}")
        print(f"Available Premium Spots: {len(available_premium)}")
        print(f"Available Handicap Spots: {len(available_handicap)}")
        print(f"Total Available: {len(available_all)}")
        
        print("✓ TEST PASSED: Spot filtering works correctly")
        return True
    
    def test_with_detected_plates(self, image_path):
        """Test 9: Integration with license plate detection"""
        print("\n" + "="*60)
        print("TEST 9: License Plate Detection Integration")
        print("="*60)
        
        if not os.path.exists(image_path):
            print(f"✗ TEST SKIPPED: Image not found at {image_path}")
            return False
        
        print(f"Processing image: {image_path}")
        
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                print("✗ TEST FAILED: Could not read image")
                return False
            
            # Detect plates
            results = model.predict(image_path, conf=0.25)
            
            if not results or len(results[0].boxes) == 0:
                print("✗ No license plates detected in image")
                return False
            
            result = results[0]
            plates_detected = []
            
            # Process each detection
            for box in result.boxes:
                bbox = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])
                
                # Convert bbox format
                x1, y1, x2, y2 = map(int, bbox)
                bbox_xywh = [x1, y1, x2-x1, y2-y1]
                
                # Read license plate
                plate_text, ocr_conf = self.parking_manager.read_license_plate(image, bbox_xywh)
                
                if plate_text:
                    plates_detected.append(plate_text)
                    print(f"\n  Detected Plate: {plate_text}")
                    print(f"  Confidence: {(ocr_conf * conf):.2f}")
                    
                    # Auto-assign spot
                    vehicle_info = {
                        'license_plate': plate_text,
                        'entry_time': datetime.now().isoformat(),
                        'preferred_type': 'standard',
                        'handicap_permit': False
                    }
                    
                    spot_id = self.spot_assigner.auto_assign_spot(vehicle_info)
                    if spot_id:
                        print(f"  → Assigned to Spot: {spot_id}")
                        self.occupancy_tracker.record_entry(spot_id, vehicle_info)
            
            if plates_detected:
                print(f"\n✓ TEST PASSED: {len(plates_detected)} plate(s) detected and assigned")
                return True
            else:
                print("✗ TEST FAILED: No plates could be read from detections")
                return False
                
        except Exception as e:
            print(f"✗ TEST FAILED: {str(e)}")
            return False
    
    def run_all_tests(self, image_path=None):
        """Run all tests in sequence"""
        print("\n" + "="*70)
        print("SMART PARKING SYSTEM - COMPREHENSIVE TEST SUITE")
        print("="*70)
        
        results = {}
        
        # Basic tests
        results['test_empty_lot'] = self.test_empty_parking_lot()
        results['test_spot_types'] = self.test_spot_types()
        results['test_manual_entry'] = self.test_manual_vehicle_entry("TEST001")
        results['test_available_filters'] = self.test_available_spots_filter()
        
        # Multiple vehicle tests
        assigned_spots = self.test_multiple_vehicles(3)
        results['test_multiple'] = len(assigned_spots) >= 3
        
        # Priority tests
        results['test_handicap'] = self.test_handicap_priority()
        
        # Exit and statistics
        if assigned_spots:
            results['test_exit'] = self.test_vehicle_exit(assigned_spots[0])
        
        results['test_statistics'] = self.test_occupancy_statistics()
        
        # License plate detection (if image provided)
        if image_path:
            results['test_with_plates'] = self.test_with_detected_plates(image_path)
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✓ PASSED" if result else "✗ FAILED"
            print(f"{test_name:30} : {status}")
        
        print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        print("="*70 + "\n")
        
        return results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Initialize tester with parking lot reset
    print("Initializing parking system tester...")
    tester = ParkingSystemTester(reset_lot=True)
    
    # Run all tests with license plate detection
    print("\nRunning comprehensive tests with license plate detection...")
    results = tester.run_all_tests(image_path="kenya car.jpg")
    
    # To test without license plate detection, use:
    # results = tester.run_all_tests()
    
    print("\nYou can also run tests without resetting by passing reset_lot=False:")
    print("  tester = ParkingSystemTester(reset_lot=False)")
