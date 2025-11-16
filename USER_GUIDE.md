# 🅿️ Smart Parking System - User Guide

## Quick Start (30 seconds)

```bash
cd e:\Zindi\smart parking
streamlit run app.py
```

Open browser → `http://localhost:8501` → Done! 🎉

---

## Overview

The Smart Parking System is a full-featured application that automates parking lot management with:

- ✅ Automatic license plate detection (AI-powered)
- ✅ Real-time parking lot visualization
- ✅ Automatic spot assignment with priority rules
- ✅ Vehicle entry/exit management
- ✅ Comprehensive history and analytics
- ✅ Interactive dashboard with live data

---

## Dashboard Features

### 🏠 Main Dashboard
**What You See:**
- 4 Key Metrics: Capacity, Occupied, Available, Utilization %
- Interactive parking lot layout (click for details)
- Current vehicles table
- Occupancy distribution chart

**Interactive Elements:**
- Hover over parking spots to see details (spot number, type, license plate)
- Color-coded status:
  - 🟢 Green = Available standard spots
  - 🔴 Red = Occupied spots
  - 🔵 Blue = Handicap spots
  - 🟡 Yellow = Premium spots

---

## Vehicle Entry Process

### Method 1: Automatic License Plate Detection (RECOMMENDED)

**Steps:**
1. Click "📸 Vehicle Entry" in sidebar
2. Click "Choose an image" button
3. Upload a photo with visible license plate
4. System automatically detects and extracts the license plate
5. Review detected plate (editable if needed)
6. Select preferred spot type: `Standard` / `Premium` / `Handicap`
7. Check `Handicap Permit` if applicable
8. Add optional notes (vehicle color, owner info, etc.)
9. Click "✅ Confirm Entry" (green button)
10. ✅ Vehicle assigned! Display shows spot number and location

**Image Tips:**
- Clear, well-lit photos work best
- Ensure license plate is fully visible
- Rear-view angle recommended
- Resolution: 640×480 or higher
- Formats: JPG, PNG, BMP

### Method 2: Manual Entry

**Steps:**
1. Scroll to "Manual Entry" section
2. Enter license plate (e.g., `KD0793`)
3. Select spot type
4. Check handicap permit if applicable
5. Click "✅ Manual Entry"
6. ✅ Vehicle assigned

**Use When:**
- Camera/image not available
- Quick entry needed
- Manual correction of detected plate

---

## Vehicle Exit Process

**Steps:**
1. Click "🚗 Vehicle Exit" in sidebar
2. Choose search method:
   - **By Spot Number**: Select spot from dropdown
   - **By License Plate**: Select vehicle license
3. Review vehicle details:
   - Parking duration (minutes)
   - Parking fee calculation
   - Entry and exit times
4. Click "✅ Confirm Exit" to complete
5. ✅ Exit recorded! Fee calculated
6. Vehicle history updated

**Fee Calculation:**
- Rate: $2.00 per hour
- Minimum charge: $2.00
- Examples:
  - 15 min → $2.00
  - 30 min → $2.00
  - 1 hour → $2.00
  - 1.5 hours → $3.00
  - 2 hours → $4.00

---

## History & Records

### 📋 Complete History

**Access:**
1. Click "📋 History" in sidebar

**Features:**
- View all parking records (chronological)
- Filter by spot type: Standard, Handicap, Premium
- Filter by status: Still Parked, Exited
- Sort by any column
- Search for specific vehicles

**Export Options:**
- 📥 Download as CSV (spreadsheet)
- 📊 Download as Excel (formatted)

**Data Shown:**
- Spot number
- License plate
- Spot type
- Entry time (date & time)
- Exit time (or "Still Parked")
- Duration in minutes

---

## Analytics & Reports

### 📊 Analytics Dashboard

**Access:**
1. Click "📊 Analytics" in sidebar

**Metrics:**
- Total vehicles today
- Average parking duration
- Current occupancy rate

**Charts:**
- Vehicles by spot type (bar chart)
- Occupancy distribution (stacked bar)

**Detailed Statistics:**
- Count of vehicles per type
- Average duration per type

**Use Cases:**
- Monitor peak hours
- Identify popular spot types
- Plan for future expansion
- Calculate daily revenue

---

## Settings & Configuration

### ⚙️ System Settings

**Access:**
1. Click "⚙️ Settings" in sidebar

**Available Options:**

1. **View Configuration**
   - Current total capacity (32 spots)
   - Distribution by type
   - Current status

2. **Reset Parking Lot**
   - ⚠️ Warning: Clears all current vehicle data
   - Confirmation required
   - Resets to empty lot

3. **Clear History**
   - ⚠️ Warning: Deletes all historical records
   - Confirmation required

4. **Export Configuration**
   - 💾 Download parking setup
   - 📅 Includes timestamp
   - JSON format for backup

5. **System Info**
   - App version
   - Last update time
   - Environment (Production)

---

## Sidebar Navigation

**Quick Stats** (Auto-updates):
- Total Spots: 32
- Occupied: Current count
- Available: Current count
- Occupancy %: Current percentage

**Refresh Button:**
- 🔄 Manually refresh all data
- Auto-refreshes every 5 seconds

**Navigation Menu:**
- 🏠 Dashboard
- 📸 Vehicle Entry
- 🚗 Vehicle Exit
- 📋 History
- 📊 Analytics
- ⚙️ Settings

---

## Spot Management

### Spot Types

**Standard Spots (28 total)**
- General-purpose parking
- Spots 1-2 in Row 1 are handicap-reserved
- Spots 3-8, 9-30 are standard

**Handicap Spots (2 total)**
- Accessible parking spaces
- Priority for handicap permit holders
- Spots 1-2 (Row 1)
- 50% discount on parking fees

**Premium Spots (2 total)**
- VIP/Priority parking
- Higher rates
- Spots 31-32 (Row 4)

### Spot Assignment Logic

**Priority Order:**
1. Handicap permit → Handicap spot
2. Preferred type available → Assigned
3. Any available spot → Assigned
4. All full → Error (No spots available)

---

## Advanced Features

### 🔔 Real-time Updates
- Dashboard refreshes automatically
- New vehicles appear immediately
- Spot status updates live

### 📊 Data Persistence
- All data saved automatically
- Survives app restart
- Files:
  - `parking_config.json` - Spot configuration
  - `parking_history.json` - Historical records
  - `parking_records.csv` - CSV export format

### 🎨 Interactive Visualizations
- Plotly charts (hover for details)
- Responsive design
- Mobile-friendly layout

### 🔍 Search & Filter
- History filtering by type
- Search by license plate
- Sort by any column
- Date range filtering

---

## Troubleshooting

### License Plate Not Detected
**Problem:** "No license plates detected"

**Solutions:**
1. ✅ Ensure plate is clearly visible
2. ✅ Try different lighting angle
3. ✅ Use higher resolution image
4. ✅ Try manual entry instead

### Vehicle Not Assigned
**Problem:** "No available spots" error

**Solutions:**
1. ✅ Check if lot is full (see dashboard)
2. ✅ Remove exited vehicles first
3. ✅ Check spot type preferences
4. ✅ Contact administrator

### Data Not Saving
**Problem:** Data lost after refresh

**Solutions:**
1. ✅ Check disk space
2. ✅ Verify write permissions
3. ✅ Restart Streamlit: `Ctrl+C` then `streamlit run app.py`
4. ✅ Check file permissions on JSON files

### Slow Performance
**Problem:** App responds slowly

**Solutions:**
1. ✅ Close other applications
2. ✅ Use smaller image files
3. ✅ Enable GPU if available
4. ✅ Clear browser cache

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `R` | Refresh data |
| `Ctrl+C` | Stop app |
| `Cmd+C` (Mac) | Stop app |
| `F5` | Refresh page |

---

## Best Practices

### For Operators:
1. ✅ Take clear photos for plate detection
2. ✅ Verify detected plates before confirming
3. ✅ Remove vehicles from system when they exit
4. ✅ Monitor dashboard regularly
5. ✅ Export history regularly for backup

### For Managers:
1. ✅ Review analytics weekly
2. ✅ Monitor peak usage times
3. ✅ Track revenue from parking fees
4. ✅ Plan maintenance based on usage
5. ✅ Export and backup data monthly

### For Maintenance:
1. ✅ Check disk space regularly
2. ✅ Monitor system performance
3. ✅ Verify backups are working
4. ✅ Update software as needed
5. ✅ Clear old temporary files

---

## Common Scenarios

### Scenario 1: Busy Parking Lot Entry

**Situation:** Multiple vehicles arriving simultaneously

**Solution:**
1. Process each vehicle one at a time
2. Use automatic detection for speed
3. Manual entry for quick confirmation
4. System handles spot assignment automatically

### Scenario 2: Vehicle Can't Find Spot

**Situation:** All spots of preferred type are full

**Solution:**
1. System automatically assigns any available spot
2. If lot is full, display error
3. Ask vehicle to return later
4. Check analytics for peak times

### Scenario 3: Lost Vehicle Records

**Situation:** Need to find a specific vehicle

**Solution:**
1. Go to History page
2. Use search/filter options
3. Can search by:
   - License plate
   - Spot number
   - Entry time
   - Vehicle type

---

## FAQ

**Q: Can I edit a license plate after detection?**
A: Yes, detected plates are editable before confirmation.

**Q: What if the wrong plate is detected?**
A: Edit the text field before confirming entry.

**Q: Can I delete a history record?**
A: Use "Clear History" in Settings (deletes all records).

**Q: Is there a parking fee limit?**
A: Minimum $2, no maximum (based on duration).

**Q: Can multiple users use the app simultaneously?**
A: Yes, but data conflicts may occur. Not recommended.

**Q: How much disk space is needed?**
A: ~50 MB for data (JSON + CSV + images)

**Q: Can I access this remotely?**
A: Yes, run on a server: `streamlit run app.py --server.address 0.0.0.0`

**Q: How long are records kept?**
A: Until manually cleared (retention: 90 days by default)

---

## Support

**For Issues:**
1. Check this guide first
2. Review troubleshooting section
3. Check system logs
4. Restart the application

**Emergency:**
- Stop app: `Ctrl+C`
- Reset lot: Settings → Reset (careful!)
- Restore backup: Use saved JSON files

---

## Tips & Tricks

### Speed Tips:
- Use keyboard + mouse for faster input
- Pre-prepare vehicle info
- Use manual entry for regulars

### Organization Tips:
- Export history weekly
- Create monthly backup
- Document peak hours
- Track revenue trends

### Accuracy Tips:
- Take photos in good lighting
- Position plate frontally
- Verify before confirming
- Update records immediately

---

**Version:** 1.0.0  
**Last Updated:** November 16, 2025  
**Status:** Production Ready ✅
