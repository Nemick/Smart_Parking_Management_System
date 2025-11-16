# 🅿️ Smart Parking System - Developer Documentation

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT FRONTEND (app.py)              │
│  ┌─────────┬──────────┬────────┬─────────┬──────────┐      │
│  │Dashboard│  Entry   │  Exit  │ History │Analytics │      │
│  └─────────┴──────────┴────────┴─────────┴──────────┘      │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼──────────┐ ┌────▼──────────┐ ┌────▼──────────┐
│ PARKING SYSTEM   │ │LICENSE PLATE  │ │  CONFIG       │
│ (parking_       │ │DETECTION      │ │ (config.py)   │
│  system.py)     │ │(read_plate_   │ │               │
│                 │ │ number.py)    │ │               │
│ Classes:        │ │               │ │               │
│ - Parking       │ │ Classes:      │ │ - Settings    │
│   Layout        │ │ - Parking     │ │ - Config      │
│ - Spot          │ │   Manager     │ │ - Database    │
│   Assigner      │ │               │ │               │
│ - Occupancy     │ │ Tools:        │ │               │
│   Tracker       │ │ - YOLOv8      │ │               │
│ - Parking       │ │ - EasyOCR     │ │               │
│   Visualizer    │ │ - OpenCV      │ │               │
└────────────────┘ └───────────────┘ └──────────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
        ┌──────────────────▼──────────────────┐
        │     DATA LAYER (JSON/CSV/Files)    │
        │ parking_config.json                │
        │ parking_history.json               │
        │ parking_records.csv                │
        └────────────────────────────────────┘
```

---

## Project Structure

```
smart parking/
│
├── FRONTEND
│   ├── app.py                    # Main Streamlit application
│   │   ├── Page: Dashboard
│   │   ├── Page: Vehicle Entry
│   │   ├── Page: Vehicle Exit
│   │   ├── Page: History
│   │   ├── Page: Analytics
│   │   └── Page: Settings
│   └── config.py                 # Configuration module
│
├── BACKEND
│   ├── parking_system.py         # Parking lot logic
│   │   ├── Class: ParkingLayout
│   │   ├── Class: SpotAssigner
│   │   ├── Class: OccupancyTracker
│   │   └── Class: ParkingVisualizer
│   │
│   └── read_plate_number.py      # Plate detection logic
│       ├── Class: ParkingManager
│       └── Functions: Detection, OCR, Processing
│
├── TESTING & UTILITY
│   ├── test.py                   # Comprehensive test suite
│   ├── startup.py                # System verification
│   └── requirements.txt           # Dependencies
│
├── DATA FILES
│   ├── parking_config.json       # Current parking state
│   ├── parking_history.json      # All records
│   └── parking_records.csv       # CSV export
│
├── MODELS & RESOURCES
│   └── trained_license_plate_detector.pt  # YOLOv8 model
│
├── DOCUMENTATION
│   ├── README.md                 # Project overview
│   ├── USER_GUIDE.md             # User manual
│   └── DEVELOPER.md              # This file
│
└── CONFIGURATION
    └── config.py                 # System configuration
```

---

## Core Classes

### 1. ParkingLayout (parking_system.py)

**Purpose:** Manages parking lot structure and spot states

**Key Methods:**
```python
__init__(config_file='parking_config.json')
  - Initialize with config file or create default

load_or_create_config()
  - Load existing or create new parking layout

create_realistic_layout()
  - Create 32 spots in 4 rows (8 per row)

save_config()
  - Persist layout to JSON

get_spot_info(spot_id)
  - Get individual spot details

get_available_spots(spot_type=None)
  - Get list of available spots, optionally filtered

occupy_spot(spot_id, vehicle_info)
  - Mark spot as occupied with vehicle data

release_spot(spot_id)
  - Mark spot as available

get_occupancy_status()
  - Get comprehensive statistics
```

**Data Structure:**
```python
{
  spot_id: {
    'row': 1-4,
    'position': 1-8,
    'side': 'north' or 'south',
    'type': 'standard' | 'handicap' | 'premium',
    'occupied': bool,
    'vehicle_info': {
      'license_plate': 'ABC123',
      'entry_time': '2025-11-16T15:30:00',
      'preferred_type': 'standard',
      'handicap_permit': bool,
      'notes': ''
    },
    'entry_time': ISO timestamp or None
  }
}
```

### 2. SpotAssigner (parking_system.py)

**Purpose:** Intelligent spot assignment

**Key Methods:**
```python
__init__(parking_layout)
  - Initialize with parking layout

auto_assign_spot(vehicle_info)
  - Automatically assign best available spot
  
  Priority:
  1. Handicap permit → Handicap spot
  2. Preferred type available → Use it
  3. Any available → Use first
  4. All full → Return None
```

### 3. OccupancyTracker (parking_system.py)

**Purpose:** Historical tracking and statistics

**Key Methods:**
```python
load_history()
  - Load from parking_history.json

save_history()
  - Persist history to file

record_entry(spot_id, vehicle_info)
  - Record vehicle entry

record_exit(spot_id)
  - Record vehicle exit time

get_statistics(period='day'|'week'|'month')
  - Get occupancy statistics for period
  
  Returns:
  {
    'total_vehicles': int,
    'avg_duration': float (minutes),
    'by_type': {
      'standard': {'count': int, 'duration_minutes': float},
      'handicap': {...},
      'premium': {...}
    }
  }
```

### 4. ParkingManager (read_plate_number.py)

**Purpose:** License plate records management

**Key Methods:**
```python
__init__(csv_path='parking_records.csv')
  - Initialize with CSV file

read_license_plate(image, bbox)
  - Extract and OCR license plate from image
  
  Returns: (plate_text, confidence)

preprocess_plate_image(img)
  - Enhance image for OCR accuracy
  - Grayscale, histogram equalization, upscaling

add_parking_record(license_plate, confidence, vehicle_image)
  - Add record to CSV

save_records()
  - Persist to CSV

get_records()
  - Return DataFrame of all records
```

---

## Data Flow

### Entry Process
```
1. User uploads image
    ↓
2. detect_license_plate_from_image()
    ├─ Load image with cv2
    ├─ Run YOLOv8 detection
    ├─ Extract plate region
    ├─ Preprocess image
    └─ Run EasyOCR
    ↓
3. Get license plate & confidence
    ↓
4. User confirms entry details
    ↓
5. Create vehicle_info dict
    ↓
6. SpotAssigner.auto_assign_spot()
    ├─ Check priorities
    ├─ Find available spot
    └─ Call occupy_spot()
    ↓
7. OccupancyTracker.record_entry()
    └─ Append to history.json
    ↓
8. ParkingManager.add_parking_record()
    └─ Append to parking_records.csv
    ↓
9. Save all changes & display confirmation
```

### Exit Process
```
1. User selects vehicle from current list
    ↓
2. Calculate parking duration
    ├─ Exit time = now
    └─ Duration = exit_time - entry_time
    ↓
3. Calculate fee
    └─ Fee = max(base_rate, duration_hours * rate)
    ↓
4. User confirms exit
    ↓
5. ParkingLayout.release_spot()
    └─ Mark occupied = False
    ↓
6. OccupancyTracker.record_exit()
    └─ Update history with exit_time
    ↓
7. Save all changes & display receipt
```

---

## API Reference

### Streamlit Pages

#### Dashboard Page
```
path: "🏠 Dashboard"
Components:
  - 4 metric cards (capacity, occupied, available, utilization)
  - Parking lot visualization (interactive)
  - Occupancy chart (stacked bar)
  - Current vehicles table
```

#### Entry Page
```
path: "📸 Vehicle Entry"
Components:
  - Image uploader
  - License plate detector
  - Manual entry fallback
  - Entry confirmation form
```

#### Exit Page
```
path: "🚗 Vehicle Exit"
Components:
  - Current vehicles dropdown
  - Vehicle details display
  - Fee calculator
  - Exit confirmation
```

#### History Page
```
path: "📋 History"
Components:
  - History data table
  - Filter controls (type, status)
  - Export buttons (CSV, Excel)
```

#### Analytics Page
```
path: "📊 Analytics"
Components:
  - Statistics metrics
  - Type utilization chart
  - Occupancy distribution
  - Detailed stats table
```

#### Settings Page
```
path: "⚙️ Settings"
Components:
  - Configuration display
  - Reset options
  - Clear history option
  - Export config button
  - System info
```

---

## Database Schema

### parking_config.json
```json
{
  "spots": {
    "1": {
      "row": 1,
      "position": 1,
      "side": "north",
      "type": "handicap",
      "occupied": false,
      "vehicle_info": null,
      "entry_time": null
    },
    ...
  }
}
```

### parking_history.json
```json
[
  {
    "spot_id": 5,
    "spot_type": "standard",
    "vehicle_info": {
      "license_plate": "ABC123",
      "entry_time": "2025-11-16T10:00:00",
      "preferred_type": "standard",
      "handicap_permit": false,
      "notes": ""
    },
    "entry_time": "2025-11-16T10:00:00",
    "exit_time": "2025-11-16T12:30:00"
  }
]
```

### parking_records.csv
```
timestamp,license_plate,confidence,vehicle_image,entry_time
2025-11-16 10:00:00,ABC123,0.95,car.jpg,2025-11-16 10:00:00
2025-11-16 10:15:00,XYZ789,0.92,car2.jpg,2025-11-16 10:15:00
```

---

## Configuration

See `config.py` for all configuration options:

```python
# Key sections:
PARKING_LOT_CONFIG         # Lot info
SPOT_DISTRIBUTION         # Type distribution
PRICING                    # Fee configuration
DETECTION_CONFIG          # YOLOv8 settings
DATABASE_CONFIG           # File paths
UI_CONFIG                 # Streamlit settings
NOTIFICATIONS             # Alert settings
ANALYTICS_CONFIG          # Stats settings
```

---

## Extending the System

### Adding a New Page

1. Create function in `app.py`:
```python
elif page == "🆕 New Page":
    st.title("New Page Title")
    # Your code here
```

2. Add to sidebar radio options:
```python
page = st.sidebar.radio(
    "Select Page:",
    [..., "🆕 New Page"]
)
```

### Adding New Spot Type

1. Update `SPOT_DISTRIBUTION` in `config.py`
2. Add color mapping in `get_spot_color()`
3. Update parking layout creation
4. Test with new type

### Integrating Payment System

1. Add payment provider API
2. Modify fee calculation in exit process
3. Store payment records
4. Update analytics

### Adding Email Notifications

1. Import `smtplib`
2. Create `send_email()` function
3. Call in entry/exit processes
4. Store email templates

---

## Testing

Run comprehensive tests:
```bash
python test.py
```

Tests included:
- Parking lot initialization
- Spot type verification
- Vehicle entry/exit
- Spot assignment logic
- Handicap priority
- Statistics generation
- License plate detection

---

## Performance Optimization

### Image Processing
- Lazy load images
- Cache detection results
- Batch processing for multiple images

### Database
- Index frequently searched fields
- Archive old records
- Compress backups

### UI
- Cache Plotly figures
- Use session state efficiently
- Lazy load data on demand

---

## Security Considerations

### Current (Basic):
- No authentication (local/trusted only)
- No encryption
- No audit logs

### Recommendations:
1. Add user authentication
2. Encrypt sensitive data
3. Add audit logging
4. Restrict file permissions
5. Use HTTPS for remote access
6. Rate limiting on API endpoints

---

## Troubleshooting Guide

### Module Import Errors
```python
# Solution: Install missing packages
pip install -r requirements.txt
```

### Model Loading Issues
```python
# Check model file exists and is readable
import os
assert os.path.exists('trained_license_plate_detector.pt')
```

### Performance Issues
```python
# Enable GPU if available
# Check torch.cuda.is_available()
# Use batch processing
```

---

## Future Roadmap

### Phase 2:
- [ ] Multi-lot support
- [ ] Reservation system
- [ ] Payment gateway
- [ ] Mobile app

### Phase 3:
- [ ] AI-powered predictions
- [ ] Real-time alerts
- [ ] Advanced analytics
- [ ] Revenue optimization

### Phase 4:
- [ ] IoT integration
- [ ] Smart gates
- [ ] License plate recognition (live)
- [ ] Automated payments

---

## Contributing Guidelines

1. Fork repository
2. Create feature branch
3. Add tests
4. Commit with clear messages
5. Push and create PR
6. Code review & merge

---

## References

- **Streamlit**: https://streamlit.io
- **YOLOv8**: https://docs.ultralytics.com
- **EasyOCR**: https://github.com/JaidedAI/EasyOCR
- **OpenCV**: https://opencv.org

---

**Version:** 1.0.0  
**Last Updated:** November 16, 2025  
**Status:** Production Ready ✅
