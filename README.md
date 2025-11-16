# 🅿️ Smart Parking System

A comprehensive smart parking management system with AI-powered license plate detection, interactive parking lot visualization, and complete vehicle tracking.

## Features

### 🎯 Core Functionality
- **📸 License Plate Detection**: Automatic detection and OCR using YOLOv8 and EasyOCR
- **🅿️ Parking Lot Management**: 32 spots organized in 4 rows with priority assignment
- **🎨 Interactive Visualization**: Real-time parking lot layout with hover details
- **📊 Analytics Dashboard**: Occupancy statistics, vehicle history, and insights
- **💾 Data Persistence**: Automatic saving of all parking records and history

### 📱 Pages & Features

#### 🏠 Dashboard
- Real-time occupancy metrics (total, occupied, available)
- Interactive parking lot layout with spot status
- Current vehicle list with entry times and duration
- Occupancy distribution by spot type

#### 📸 Vehicle Entry
- **Image Upload**: Upload vehicle images for automatic plate detection
- **Manual Entry**: Option to manually enter license plate
- **Smart Assignment**: Intelligent spot allocation based on:
  - Vehicle type preference (standard/premium/handicap)
  - Handicap permit priority
  - Spot availability
- **Confirmation**: Displays assigned spot with entry time

#### 🚗 Vehicle Exit
- **Search Options**: Find vehicle by spot number or license plate
- **Duration Tracking**: Shows parking duration in minutes
- **Fee Calculation**: Automatic parking fee calculation ($2/hour)
- **Exit Record**: Records exit time for history

#### 📋 History
- Complete parking history with timestamps
- Filter by spot type and status (exited/still parked)
- Export to CSV or Excel
- Search and sort capabilities

#### 📊 Analytics
- Daily vehicle statistics
- Spot type utilization analysis
- Average parking duration by type
- Visual charts and graphs

#### ⚙️ Settings
- System configuration and status
- Reset parking lot
- Clear history
- Export configuration

## Installation

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)
- GPU support (optional, for faster plate detection)

### Setup Instructions

1. **Clone/Download the project**
```bash
cd e:\Zindi\smart parking
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the Streamlit app**
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## Project Structure

```
smart parking/
├── app.py                              # Streamlit frontend
├── parking_system.py                   # Backend: parking lot management
├── read_plate_number.py               # Backend: license plate detection
├── test.py                             # Test suite
├── parking_config.json                 # Spot configuration
├── parking_history.json                # Historical records
├── parking_records.csv                 # CSV records
├── trained_license_plate_detector.pt  # YOLOv8 model
├── requirements.txt                    # Dependencies
└── README.md                           # This file
```

## Key Modules

### `parking_system.py`
**Main Classes:**
- `ParkingLayout`: Manages parking lot structure (32 spots in 4 rows)
- `SpotAssigner`: Intelligent spot assignment algorithm
- `OccupancyTracker`: Historical data and statistics
- `ParkingVisualizer`: Interactive visualization

### `read_plate_number.py`
**Main Classes:**
- `ParkingManager`: CSV records management
- License plate detection using YOLOv8
- OCR processing with EasyOCR
- Image preprocessing and enhancement

### `app.py`
**Streamlit Frontend with:**
- 6 main pages (Dashboard, Entry, Exit, History, Analytics, Settings)
- Real-time data updates
- Interactive charts and visualizations
- File upload and download capabilities

## Usage Guide

### Adding a Vehicle (Entry)

**Method 1: Automatic Detection**
1. Go to "📸 Vehicle Entry"
2. Click "Choose an image" and upload vehicle photo
3. System detects and displays license plate
4. Select spot type and handicap status if applicable
5. Click "Confirm Entry"

**Method 2: Manual Entry**
1. Go to "📸 Vehicle Entry"
2. Scroll to "Manual Entry" section
3. Enter license plate manually
4. Select spot type
5. Click "Manual Entry"

### Removing a Vehicle (Exit)

1. Go to "🚗 Vehicle Exit"
2. Search by Spot Number or License Plate
3. Review parking duration and fee
4. Click "Confirm Exit"
5. Record is automatically added to history

### Viewing Records

- **Dashboard**: Quick overview of current status
- **History**: Complete record of all vehicles with timestamps
- **Analytics**: Daily statistics and insights

## Parking Lot Layout

```
ROW 1 (North - Facing Down)
[♿1] [♿2] [3] [4] [5] [6] [7] [8]    <- Handicap Spots: 1-2

ROW 2 (South - Facing Up)
[9] [10] [11] [12] [13] [14] [15] [16]

ROW 3 (North - Facing Down)
[17] [18] [19] [20] [21] [22] [23] [24]

ROW 4 (South - Facing Up)
[25] [26] [27] [28] [29] [30] [⭐31] [⭐32]   <- Premium Spots: 31-32
```

## Spot Types

- **Standard**: General parking (28 spots)
- **Handicap**: Accessible parking (2 spots, spots 1-2)
- **Premium**: Priority/VIP parking (2 spots, spots 31-32)

## Parking Fees

- Base rate: $2.00 per hour
- Minimum charge: $2.00 (regardless of duration)
- Example: 30 minutes = $2.00, 60 minutes = $2.00, 90 minutes = $3.00

## Technical Details

### License Plate Detection
- **Model**: YOLOv8 trained model
- **Confidence Threshold**: 25% (0.25)
- **OCR Engine**: EasyOCR (English)
- **Preprocessing**: 
  - Grayscale conversion
  - Histogram equalization
  - 2x upscaling for better OCR accuracy

### Data Storage
- **Parking Configuration**: `parking_config.json`
- **History Records**: `parking_history.json`
- **CSV Export**: `parking_records.csv`

## Troubleshooting

### License Plate Not Detected
- Ensure image is clear and well-lit
- License plate should be visible in frame
- Try uploading a different angle or higher resolution

### Spot Assignment Fails
- Check if parking lot is full (max 32 vehicles)
- Try selecting a different spot type
- Use manual entry as alternative

### Streamlit Not Starting
- Verify Python 3.8+ installed
- Check all dependencies: `pip list`
- Reinstall if needed: `pip install -r requirements.txt --force-reinstall`

## Future Enhancements

- [ ] Mobile app support
- [ ] Email/SMS notifications
- [ ] Multi-lot support
- [ ] Reservation system
- [ ] Payment gateway integration
- [ ] Real-time alerts
- [ ] Advanced analytics with ML predictions
- [ ] Camera feed integration

## Performance Notes

- First run loads models: ~10-20 seconds
- Subsequent runs: ~2-3 seconds per image
- GPU support available for faster processing
- Batch processing for multiple images

## Credits

Built with:
- **Streamlit**: Web framework
- **YOLOv8**: Object detection
- **EasyOCR**: Text recognition
- **OpenCV**: Image processing
- **Plotly**: Interactive visualizations
- **Pandas**: Data handling

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review test output: `python test.py`
3. Check log files in workspace

---

**Version**: 1.0.0  
**Last Updated**: November 16, 2025  
**Status**: Production Ready ✅
