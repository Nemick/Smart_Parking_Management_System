"""
Smart Parking System - Streamlit Frontend
Full-featured parking management application with license plate detection
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os
from PIL import Image
import cv2
import numpy as np
import io

# Import backend modules
from parking_system import ParkingLayout, SpotAssigner, OccupancyTracker
from read_plate_number import ParkingManager, model
from config import SYSTEM_STATUS
import easyocr

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Smart Parking System",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Premium Design with Harmonious Colors
st.markdown("""
<style>
    /* Modern color palette with better harmony */
    :root {
        --primary: #0D47A1;      /* Deep blue */
        --secondary: #FF6F00;    /* Vibrant orange */
        --accent: #1976D2;       /* Professional blue */
        --success: #00C853;      /* Pure green */
        --warning: #FFA000;      /* Golden orange */
        --danger: #D32F2F;       /* Deep red */
        --light: #F5F5F5;        /* Light gray */
        --dark: #212121;         /* Dark gray */
    }
    
    /* Main container - Clean gradient */
    .main {
        padding-top: 2rem;
        background: linear-gradient(180deg, #FAFAFA 0%, #F5F5F5 100%);
        min-height: 100vh;
    }
    
    /* Headers - Better text contrast */
    h1 {
        color: #0D47A1;
        font-weight: 800;
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    
    h2 {
        color: #1565C0;
        font-weight: 700;
        font-size: 1.8em;
    }
    
    h3 {
        color: #1976D2;
        font-weight: 600;
        font-size: 1.3em;
    }
    
    /* Success card - Vibrant green */
    .success-card {
        background: linear-gradient(135deg, #00C853 0%, #00B24D 100%);
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #00AA47;
        box-shadow: 0 4px 12px rgba(0, 200, 83, 0.25);
        color: white;
        font-weight: 600;
    }
    
    /* Warning card - Golden orange */
    .warning-card {
        background: linear-gradient(135deg, #FFA000 0%, #FF8F00 100%);
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #FF6F00;
        box-shadow: 0 4px 12px rgba(255, 160, 0, 0.25);
        color: #FFF;
        font-weight: 600;
    }
    
    /* Error card - Deep red */
    .error-card {
        background: linear-gradient(135deg, #D32F2F 0%, #C62828 100%);
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #B71C1C;
        box-shadow: 0 4px 12px rgba(211, 47, 47, 0.25);
        color: white;
        font-weight: 600;
    }
    
    /* Info card - Professional blue */
    .info-card {
        background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #0D47A1;
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.25);
        color: white;
        font-weight: 600;
    }
    
    /* Metric cards - Clean design */
    .metric-card {
        background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.2);
        color: white;
    }
    
    /* Button styling - Solid colors */
    .stButton > button {
        background: linear-gradient(135deg, #0D47A1 0%, #1565C0 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(13, 71, 161, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(13, 71, 161, 0.4);
        background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%);
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border: 2px solid #1976D2 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    
    /* Sidebar - Dark professional */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D47A1 0%, #1565C0 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white;
    }
    
    /* Radio button styling */
    .stRadio > label {
        background: linear-gradient(135deg, #F5F5F5 0%, #EEEEEE 100%);
        padding: 15px 20px;
        border-radius: 8px;
        border: 2px solid #1976D2;
        font-weight: 600;
        color: #0D47A1;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .stRadio > label:hover {
        background: linear-gradient(135deg, #EEEEEE 0%, #E0E0E0 100%);
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.2);
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        font-weight: 600;
        color: #0D47A1;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(13, 71, 161, 0.15);
    }
    
    /* Divider */
    hr {
        border: 0;
        height: 2px;
        background: linear-gradient(90deg, #0D47A1 0%, #FF6F00 50%, #0D47A1 100%);
    }
    
    /* Navigation button styling */
    .nav-button {
        background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 5px;
    }
    
    .nav-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3);
    }
    
    .nav-button.active {
        background: linear-gradient(135deg, #0D47A1 0%, #1976D2 100%);
        box-shadow: 0 6px 16px rgba(13, 71, 161, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'parking_layout' not in st.session_state:
    st.session_state.parking_layout = ParkingLayout()
    st.session_state.spot_assigner = SpotAssigner(st.session_state.parking_layout)
    st.session_state.occupancy_tracker = OccupancyTracker(st.session_state.parking_layout)
    st.session_state.parking_manager = ParkingManager()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_spot_color(spot):
    """Determine color based on spot status and type"""
    if spot['occupied']:
        return '#FF6B6B'  # Red for occupied
    elif spot['type'] == 'handicap':
        return '#87CEEB'  # Sky blue for handicap
    elif spot['type'] == 'premium':
        return '#FFD700'  # Gold for premium
    else:
        return '#90EE90'  # Green for available

def get_all_parked_vehicles():
    """Get list of all currently parked license plates"""
    parked_plates = []
    for spot in st.session_state.parking_layout.spots.values():
        if spot['occupied'] and spot['vehicle_info']:
            plate = spot['vehicle_info'].get('license_plate', '').upper()
            if plate:
                parked_plates.append(plate)
    return parked_plates

def is_plate_already_parked(plate_text):
    """Check if a license plate is already parked"""
    parked_plates = get_all_parked_vehicles()
    return plate_text.upper() in parked_plates

def detect_license_plate_from_image(image_path):
    """Detect and extract license plate from image"""
    try:
        image = cv2.imread(image_path)
        if image is None:
            return None, None, "Error: Could not read image"
        
        results = model.predict(image_path, conf=0.25)
        
        if not results or len(results[0].boxes) == 0:
            return None, None, "No license plates detected"
        
        result = results[0]
        plates_info = []
        
        for box in result.boxes:
            bbox = box.xyxy[0].cpu().numpy()
            conf = float(box.conf[0])
            
            x1, y1, x2, y2 = map(int, bbox)
            bbox_xywh = [x1, y1, x2-x1, y2-y1]
            
            plate_text, ocr_conf = st.session_state.parking_manager.read_license_plate(
                image, bbox_xywh
            )
            
            if plate_text:
                plates_info.append({
                    'plate': plate_text,
                    'confidence': ocr_conf * conf,
                    'bbox': (x1, y1, x2, y2)
                })
        
        if not plates_info:
            return None, None, "License plate detected but could not read text"
        
        # Return the plate with highest confidence
        best_plate = max(plates_info, key=lambda x: x['confidence'])
        return best_plate['plate'], best_plate['confidence'], "Success"
        
    except Exception as e:
        return None, None, f"Error: {str(e)}"

def draw_parking_lot_visualization():
    """Create interactive parking lot visualization"""
    spots = st.session_state.parking_layout.spots
    
    # Prepare data for visualization
    fig = go.Figure()
    
    spot_rows = {1: [], 2: [], 3: [], 4: []}
    
    for spot_id, spot in spots.items():
        row = spot['row']
        col = spot['position']
        
        color = get_spot_color(spot)
        hover_text = f"<b>Spot {spot_id}</b><br>"
        hover_text += f"Type: {spot['type'].title()}<br>"
        hover_text += f"Status: {'Occupied' if spot['occupied'] else 'Available'}"
        
        if spot['occupied'] and spot['vehicle_info']:
            hover_text += f"<br>License: {spot['vehicle_info'].get('license_plate', 'N/A')}"
        
        fig.add_trace(go.Scatter(
            x=[col],
            y=[row],
            mode='markers',
            marker=dict(
                size=40,
                color=color,
                line=dict(color='black', width=2),
                symbol='square'
            ),
            text=[hover_text],
            hovertemplate='%{text}<extra></extra>',
            showlegend=False,
            name=f'Spot {spot_id}'
        ))
        
        # Add spot number
        fig.add_annotation(
            x=col,
            y=row,
            text=str(spot_id),
            showarrow=False,
            font=dict(size=12, color='black', family='Arial Black'),
            xanchor='center',
            yanchor='middle'
        )
        
        # Add license plate if occupied
        if spot['occupied'] and spot['vehicle_info']:
            plate = spot['vehicle_info'].get('license_plate', 'N/A')
            fig.add_annotation(
                x=col,
                y=row - 0.25,
                text=f"<i>{plate}</i>",
                showarrow=False,
                font=dict(size=8, color='white'),
                xanchor='center',
                yanchor='middle',
                bgcolor='rgba(0,0,0,0.5)',
                borderpad=2
            )
    
    fig.update_layout(
        title="<b>Parking Lot Layout</b>",
        xaxis=dict(
            title="Position",
            showgrid=True,
            zeroline=False,
            range=[0, 9]
        ),
        yaxis=dict(
            title="Row",
            showgrid=True,
            zeroline=False,
            range=[0.5, 4.5]
        ),
        height=500,
        hovermode='closest',
        plot_bgcolor='#f8f9fa',
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def create_occupancy_chart():
    """Create occupancy statistics chart"""
    status = st.session_state.parking_layout.get_occupancy_status()
    
    # By type pie chart
    by_type = status['by_type']
    types = []
    occupied = []
    available = []
    
    for spot_type in ['standard', 'handicap', 'premium']:
        types.append(spot_type.title())
        occupied.append(by_type[spot_type]['occupied'])
        available.append(by_type[spot_type]['total'] - by_type[spot_type]['occupied'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=types,
        y=occupied,
        name='Occupied',
        marker_color='#FF6B6B'
    ))
    
    fig.add_trace(go.Bar(
        x=types,
        y=available,
        name='Available',
        marker_color='#90EE90'
    ))
    
    fig.update_layout(
        title="<b>Occupancy by Spot Type</b>",
        barmode='stack',
        height=400,
        hovermode='x unified',
        plot_bgcolor='#f8f9fa'
    )
    
    return fig

def display_current_vehicles():
    """Display all currently parked vehicles"""
    spots = st.session_state.parking_layout.spots
    current_vehicles = []
    
    for spot_id, spot in spots.items():
        if spot['occupied'] and spot['vehicle_info']:
            entry_time = datetime.fromisoformat(spot['entry_time'])
            duration = datetime.now() - entry_time
            
            current_vehicles.append({
                'Spot': spot_id,
                'License Plate': spot['vehicle_info'].get('license_plate', 'N/A'),
                'Type': spot['type'].title(),
                'Entry Time': entry_time.strftime('%H:%M:%S'),
                'Duration (min)': int(duration.total_seconds() / 60),
                'Row': spot['row']
            })
    
    if current_vehicles:
        df = pd.DataFrame(current_vehicles).sort_values('Spot')
        return df
    else:
        return None

# ============================================================================
# SIDEBAR
# ============================================================================

st.sidebar.markdown(f"""
<div style='background: linear-gradient(135deg, #0D47A1 0%, #1565C0 100%); 
            padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(13, 71, 161, 0.3);'>
    <h1 style='color: white; margin: 0; font-size: 3em;'>🅿️</h1>
    <h2 style='color: white; margin: 10px 0 0 0; font-size: 1.4em; letter-spacing: 1px;'>Smart Parking</h2>
    <p style='color: rgba(255,255,255,0.95); margin: 8px 0 0 0; font-size: 0.95em; letter-spacing: 0.5px;'>System v{SYSTEM_STATUS['version']}</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Quick action buttons
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

st.sidebar.markdown("---")
# Navigation menu - Enhanced styling
st.sidebar.markdown("""
<div style='background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%); 
            padding: 20px; border-radius: 12px; margin: 10px 0;
            border: 1px solid rgba(255,255,255,0.15); backdrop-filter: blur(10px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);'>
    <h3 style='color: white; margin: 0 0 20px 0; font-size: 1.15em; font-weight: 700; 
               letter-spacing: 0.5px; text-transform: uppercase;'>🗺️ Navigation Menu</h3>
    <style>
        /* Navigation radio button styling */
        .nav-menu label {
            display: block;
            width: 100%;
            padding: 14px 16px;
            margin-bottom: 8px;
            background: linear-gradient(90deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
            border: 1.5px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            color: white;
            font-weight: 600;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .nav-menu label:hover {
            background: linear-gradient(90deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.05) 100%);
            border-color: rgba(255,255,255,0.25);
            transform: translateX(4px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }
        
        .nav-menu label:active {
            transform: translateX(2px);
        }
    </style>
    <div class='nav-menu'>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Select Page:",
    [
        "🏢 Dashboard",
        "🚗 Vehicle Entry",
        "🚪 Vehicle Exit",
        "📜 History",
        "📈 Analytics",
        "⚙️ Settings"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

# Status indicator with better colors
st.sidebar.markdown("---")
status = st.session_state.parking_layout.get_occupancy_status()
occupancy_pct = status['occupancy_rate']
if occupancy_pct >= 90:
    st.sidebar.markdown("""
    <div class="warning-card" style='margin: 10px 0;'>
        ⚠️ <b>Lot Nearly Full</b> - Only {:.0f} spots left
    </div>
    """.format(status['available_spots']), unsafe_allow_html=True)
elif occupancy_pct >= 70:
    st.sidebar.markdown("""
    <div class="info-card" style='margin: 10px 0;'>
        📊 <b>70% Capacity</b> - {:.0f} spots available
    </div>
    """.format(status['available_spots']), unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
    <div class="success-card" style='margin: 10px 0;'>
        {:.0f} spots Available
    </div>
    """.format(status['available_spots']), unsafe_allow_html=True)

st.sidebar.markdown("---")
# ============================================================================
# PAGE: DASHBOARD
# ============================================================================

if page == "🏢 Dashboard":
    st.title("🏠 Smart Parking Dashboard")
    st.markdown("### Real-time Parking Management System")
    st.markdown("---")
    
    # Get current status
    status = st.session_state.parking_layout.get_occupancy_status()
    
    # Key Metrics with enhanced styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 25px; border-radius: 15px; text-align: center;
                    box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 2em;'>🅿️</h3>
            <p style='color: white; margin: 5px 0 0 0; font-size: 1.2em; font-weight: bold;'>Total Capacity</p>
            <p style='color: white; margin: 5px 0 0 0; font-size: 2.5em; font-weight: 700;'>"""+str(status['total_spots'])+"""</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        occupy_pct = status['occupancy_rate']
        color = '#FF6B35' if occupy_pct > 70 else '#2ECC71'
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {color} 0%, #FF8C42 100%); 
                    padding: 25px; border-radius: 15px; text-align: center;
                    box-shadow: 0 8px 16px rgba(255, 107, 53, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 2em;'>🚗</h3>
            <p style='color: white; margin: 5px 0 0 0; font-size: 1.2em; font-weight: bold;'>Currently Occupied</p>
            <p style='color: white; margin: 5px 0 0 0; font-size: 2.5em; font-weight: 700;'>{status['occupied_spots']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avail_color = '#2ECC71' if status['available_spots'] > 5 else '#F39C12'
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {avail_color} 0%, #27AE60 100%); 
                    padding: 25px; border-radius: 15px; text-align: center;
                    box-shadow: 0 8px 16px rgba(46, 204, 113, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 2em;'>✅</h3>
            <p style='color: white; margin: 5px 0 0 0; font-size: 1.2em; font-weight: bold;'>Available Spots</p>
            <p style='color: white; margin: 5px 0 0 0; font-size: 2.5em; font-weight: 700;'>{status['available_spots']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%); 
                    padding: 25px; border-radius: 15px; text-align: center;
                    box-shadow: 0 8px 16px rgba(52, 152, 219, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 2em;'>📊</h3>
            <p style='color: white; margin: 5px 0 0 0; font-size: 1.2em; font-weight: bold;'>Utilization</p>
            <p style='color: white; margin: 5px 0 0 0; font-size: 2.5em; font-weight: 700;'>{status['occupancy_rate']:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main visualizations
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🅿️ Parking Lot Layout")
        fig_lot = draw_parking_lot_visualization()
        st.plotly_chart(fig_lot, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Occupancy by Type")
        fig_occupancy = create_occupancy_chart()
        st.plotly_chart(fig_occupancy, use_container_width=True)
    
    st.markdown("---")
    
    # Status Indicator
    if status['occupancy_rate'] >= 90:
        st.markdown("""
        <div class="warning-card">
            ⚠️ <b>Parking Lot Nearly Full!</b> - Only a few spots remaining
        </div>
        """, unsafe_allow_html=True)
    elif status['available_spots'] == 0:
        st.markdown("""
        <div class="error-card">
            🔴 <b>Parking Lot is FULL!</b> - No available spots
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-card">
            🟢 <b>Parking Lot Operating Normally</b> - {status['available_spots']} spots available
        </div>
        """, unsafe_allow_html=True)
    
    # Currently Parked Vehicles
    st.markdown("---")
    st.subheader("🚗 Currently Parked Vehicles")
    current_df = display_current_vehicles()
    
    if current_df is not None:
        st.dataframe(current_df, use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div class="info-card">
            ✨ <b>No vehicles currently in the parking lot</b>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE: VEHICLE ENTRY
# ============================================================================

elif page == "🚗 Vehicle Entry":
    st.title("📸 Vehicle Entry - License Plate Detection")
    st.markdown("### 🎯 Add a new vehicle to the parking lot")
    
    # Choose input method
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.info("**📷 Input Method**")
    
    input_method = st.radio(
        "How would you like to capture the image?",
        ["📁 Upload Image", "📹 Webcam Capture"],
        horizontal=True,
        key="input_method"
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns([1.2, 0.8])
    
    captured_image_path = None
    captured_image = None
    
    # Method 1: Upload File
    if input_method == "📁 Upload Image":
        with col1:
            st.markdown("#### 📁 Upload Vehicle Image")
            st.write("Upload a clear image of the vehicle's license plate or rear view")
            
            uploaded_file = st.file_uploader(
                "Choose an image...",
                type=['jpg', 'jpeg', 'png', 'bmp'],
                key="vehicle_entry"
            )
            
            if uploaded_file is not None:
                # Save uploaded file with unique name (prevent auto-download)
                import uuid
                unique_id = str(uuid.uuid4())[:8]
                captured_image_path = f"temp_vehicle_{unique_id}.jpg"
                with open(captured_image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Display image
                captured_image = Image.open(captured_image_path)
                st.image(captured_image, caption="📸 Uploaded Image", use_container_width=True)
    
    # Method 2: Webcam Capture
    elif input_method == "📹 Webcam Capture":
        with col1:
            st.markdown("#### 📹 Capture from Webcam")
            st.write("Click 'Take Picture' to capture an image from your webcam")
            
            picture = st.camera_input("Take a picture", key="camera_input")
            
            if picture is not None:
                # Save webcam capture
                captured_image = Image.open(picture)
                import uuid
                unique_id = str(uuid.uuid4())[:8]
                captured_image_path = f"temp_webcam_{unique_id}.jpg"
                captured_image.save(captured_image_path)
                st.image(captured_image, caption="📸 Captured Image", use_container_width=True)
    
    # Process image if captured
    if captured_image_path and os.path.exists(captured_image_path):
        # Detect plate
        with st.spinner("🔍 Detecting license plate..."):
            plate_text, confidence, message = detect_license_plate_from_image(captured_image_path)
        
        if plate_text:
            # Check for duplicates BEFORE showing form
            if is_plate_already_parked(plate_text):
                st.error(f"""
                ⚠️ **Vehicle Already Parked!**
                
                License plate **{plate_text.upper()}** is already in the parking lot.
                
                - **Please use Vehicle Exit** to check out the existing vehicle first
                - Or verify you have the correct license plate
                """)
                # Clean up temp file
                try:
                    if os.path.exists(captured_image_path):
                        os.remove(captured_image_path)
                except:
                    pass
            else:
                st.markdown("""
                <div class="success-card">
                    ✅ License plate detected successfully!
                </div>
                """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("#### 📋 Entry Details")
                    st.markdown("---")
                    
                    detected_plate = st.text_input(
                        "License Plate:",
                        value=plate_text,
                        disabled=False,
                        key="detected_plate_entry"
                    )
                    
                    col_conf1, col_conf2 = st.columns(2)
                    with col_conf1:
                        st.metric("🎯 Confidence", f"{confidence:.1%}")
                    
                    col_type1, col_type2 = st.columns(2)
                    with col_type1:
                        spot_type = st.selectbox(
                            "Spot Type:",
                            ["standard", "premium", "handicap"],
                            key="entry_spot_type"
                        )
                    
                    with col_type2:
                        has_handicap = st.checkbox("♿ Handicap Permit", value=False)
                    
                    vehicle_notes = st.text_area(
                        "📝 Vehicle Notes (Optional):",
                        placeholder="Color, model, owner info, etc.",
                        height=80
                    )
                    
                    st.markdown("---")
                    
                    # Entry button with confirmation
                    if st.button("✅ Confirm Entry", width='stretch', type="primary"):
                        # Final duplicate check before confirming
                        final_plate = detected_plate.upper()
                        
                        if is_plate_already_parked(final_plate):
                            st.error(f"❌ **ERROR**: Plate {final_plate} is already parked!")
                        else:
                            vehicle_info = {
                                'license_plate': final_plate,
                                'entry_time': datetime.now().isoformat(),
                                'preferred_type': spot_type,
                                'handicap_permit': has_handicap,
                                'notes': vehicle_notes
                            }
                            
                            # Assign spot
                            spot_id = st.session_state.spot_assigner.auto_assign_spot(vehicle_info)
                            
                            if spot_id:
                                # Record entry
                                st.session_state.occupancy_tracker.record_entry(spot_id, vehicle_info)
                                
                                # Add to parking records
                                file_source = "webcam" if input_method == "📹 Webcam Capture" else "upload"
                                st.session_state.parking_manager.add_parking_record(
                                    final_plate,
                                    confidence,
                                    f"{file_source}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                                )
                                
                                # Success message with styling
                                st.markdown(f"""
                                <div class="success-card">
                                    ✅ Vehicle Successfully Parked!
                                    
                                    📋 License Plate: {final_plate}
                                    
                                    🅿️ Assigned Spot: {spot_id}
                                    
                                    🕐 Entry Time: {datetime.now().strftime('%H:%M:%S')}
                                    
                                    📸 Source: {input_method}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Display spot info
                                spot_info = st.session_state.parking_layout.get_spot_info(spot_id)
                                st.markdown(f"""
                                <div class="info-card">
                                    📍 <b>Spot Details:</b> Spot {spot_id} - Row {spot_info['row']}, Type: {spot_info['type'].title()}
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <div class="error-card">
                                    ❌ <b>Parking lot is full!</b> No available spots at the moment.
                                </div>
                                """, unsafe_allow_html=True)
                    
                    # Clean up temp file after processing
                    try:
                        if os.path.exists(captured_image_path):
                            os.remove(captured_image_path)
                    except:
                        pass
        else:
            st.markdown(f"""
            <div class="error-card">
                ❌ <b>Detection Failed</b><br>
                {message}
            </div>
            """, unsafe_allow_html=True)
            st.warning("💡 **Try uploading a clearer image** of the license plate for better detection")
            try:
                if os.path.exists(captured_image_path):
                    os.remove(captured_image_path)
            except:
                pass
    
    # Manual entry option
    st.markdown("---")
    st.subheader("📝 Manual Entry (Without Image)")
    st.write("Enter vehicle details manually if image detection isn't available")
    
    col1, col2 = st.columns(2)
    
    with col1:
        manual_plate = st.text_input(
            "License Plate:",
            placeholder="e.g., KD0793",
            key="manual_entry_plate"
        )
    
    with col2:
        manual_spot_type = st.selectbox(
            "Spot Type:",
            ["standard", "premium", "handicap"],
            key="manual_type"
        )
    
    manual_handicap = st.checkbox("♿ Handicap Permit", value=False, key="manual_handicap")
    
    if st.button("✅ Manual Entry", width='stretch', key="manual_entry_btn"):
        if manual_plate:
            final_manual_plate = manual_plate.upper()
            
            # Check for duplicates
            if is_plate_already_parked(final_manual_plate):
                st.markdown(f"""
                <div class="error-card">
                    ⚠️ <b>Vehicle Already Parked!</b><br>
                    License plate <b>{final_manual_plate}</b> is already in the parking lot.
                </div>
                """, unsafe_allow_html=True)
            else:
                vehicle_info = {
                    'license_plate': final_manual_plate,
                    'entry_time': datetime.now().isoformat(),
                    'preferred_type': manual_spot_type,
                    'handicap_permit': manual_handicap,
                    'notes': 'Manual entry'
                }
                
                spot_id = st.session_state.spot_assigner.auto_assign_spot(vehicle_info)
                
                if spot_id:
                    st.session_state.occupancy_tracker.record_entry(spot_id, vehicle_info)
                    st.session_state.parking_manager.add_parking_record(
                        final_manual_plate,
                        0.95,
                        "manual_entry"
                    )
                    
                    st.markdown(f"""
                    <div class="success-card">
                        ✅ <b>Vehicle Successfully Parked!</b><br>
                        Vehicle {final_manual_plate} assigned to Spot {spot_id}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="error-card">
                        ❌ <b>Parking lot is full!</b>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("❌ Please enter a license plate")

# ============================================================================
# PAGE: VEHICLE EXIT
# ============================================================================

elif page == "🚪 Vehicle Exit":
    st.title("🚗 Vehicle Exit Management")
    
    # Get current vehicles
    current_df = display_current_vehicles()
    
    if current_df is not None and len(current_df) > 0:
        st.subheader("🔍 Select Vehicle to Exit")
        
        # Create a selection interface
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_type = st.radio("Search by:", ["Spot Number", "License Plate"])
        
        with col2, col3:
            pass
        
        if search_type == "Spot Number":
            spot_options = current_df['Spot'].tolist()
            selected_spot = st.selectbox("Select Spot:", spot_options)
            selected_vehicle = current_df[current_df['Spot'] == selected_spot].iloc[0]
        else:
            plate_options = current_df['License Plate'].tolist()
            selected_plate = st.selectbox("Select License Plate:", plate_options)
            selected_vehicle = current_df[current_df['License Plate'] == selected_plate].iloc[0]
            selected_spot = selected_vehicle['Spot']
        
        # Display vehicle details
        st.markdown("---")
        st.subheader("📋 Vehicle Details")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Spot", selected_vehicle['Spot'])
        with col2:
            st.metric("License Plate", selected_vehicle['License Plate'])
        with col3:
            st.metric("Spot Type", selected_vehicle['Type'])
        with col4:
            st.metric("Duration (min)", selected_vehicle['Duration (min)'])
        
        # Entry and exit times
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Entry Time:** {selected_vehicle['Entry Time']}")
        with col2:
            exit_time = datetime.now().strftime('%H:%M:%S')
            st.write(f"**Exit Time:** {exit_time}")
        
        # Parking fee calculation (Ksh. 100 per hour)
        duration_hours = selected_vehicle['Duration (min)'] / 60
        parking_fee = max(100, round(duration_hours * 100, 2))
        
        st.markdown("---")
        st.subheader("💰 Parking Fee")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Duration", f"{selected_vehicle['Duration (min)']} min")
        with col2:
            st.metric("Rate", "Ksh. 100/hour")
        with col3:
            st.metric("Total Fee", f"Ksh.{parking_fee:.2f}")
        
        # Exit confirmation
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("✅ Confirm Exit", width='stretch', type="primary"):
                # Process exit
                st.session_state.parking_layout.release_spot(selected_spot)
                st.session_state.occupancy_tracker.record_exit(selected_spot)
                
                st.success(f"""
                ✅ **Vehicle Successfully Exited!**
                
                - **License Plate:** {selected_vehicle['License Plate']}
                - **Spot:** {selected_spot}
                - **Total Duration:** {selected_vehicle['Duration (min)']} minutes
                - **Parking Fee:** Ksh.{parking_fee:.2f}
                """)
                
                st.info("Thank you for using our parking lot!")
        
        with col2:
            if st.button("❌ Cancel", width='stretch'):
                st.info("Exit cancelled")
    
    else:
        st.info("ℹ️ No vehicles currently in the parking lot")

# ============================================================================
# PAGE: HISTORY
# ============================================================================

elif page == "📜 History":
    st.title("📋 Parking History & Records")
    
    # Initialize session state for export
    if 'history_csv' not in st.session_state:
        st.session_state.history_csv = None
    if 'history_excel' not in st.session_state:
        st.session_state.history_excel = None
    
    # Load history
    history = st.session_state.occupancy_tracker.history
    
    if history:
        # Convert to dataframe
        history_data = []
        for entry in history:
            # Determine status
            status = 'Exited' if entry['exit_time'] else 'Still Parked'
            
            # Calculate duration in hours
            if entry['exit_time']:
                duration_seconds = (datetime.fromisoformat(entry['exit_time']) - 
                                   datetime.fromisoformat(entry['entry_time'])).total_seconds()
                duration_hours = duration_seconds / 3600
                duration_display = f"{duration_hours:.2f} hrs"
            else:
                duration_display = "Still Parked"
            
            history_data.append({
                'Spot': entry['spot_id'],
                'License Plate': entry['vehicle_info'].get('license_plate', 'N/A'),
                'Type': entry['spot_type'].title(),
                'Entry Time': entry['entry_time'],
                'Exit Time': entry['exit_time'] if entry['exit_time'] else 'Still Parked',
                'Status': status,
                'Duration (Hours)': duration_display
            })
        
        history_df = pd.DataFrame(history_data).sort_values('Entry Time', ascending=False)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_type = st.multiselect(
                "Filter by Spot Type:",
                ['Standard', 'Handicap', 'Premium'],
                default=['Standard', 'Handicap', 'Premium']
            )
        
        with col2:
            filter_status = st.multiselect(
                "Filter by Status:",
                ['Still Parked', 'Exited'],
                default=['Still Parked', 'Exited']
            )
        
        with col3:
            days_back = st.number_input("Days to show:", min_value=1, max_value=90, value=7)
        
        # Apply filters - Fixed logic to use Status column
        filtered_df = history_df[
            (history_df['Type'].isin(filter_type)) &
            (history_df['Status'].isin(filter_status))
        ].copy()
        
        # Display table
        st.subheader(f"Total Records: {len(filtered_df)}")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        # Export option
        st.markdown("---")
        st.subheader("📥 Export Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Prepare CSV Export", use_container_width=True):
                st.session_state.history_csv = filtered_df.to_csv(index=False)
                st.success("✅ CSV ready for download!")
        
        with col2:
            if st.button("🔄 Prepare Excel Export", use_container_width=True):
                try:
                    from io import BytesIO
                    excel_buffer = BytesIO()
                    filtered_df.to_excel(excel_buffer, index=False, engine='openpyxl')
                    excel_buffer.seek(0)
                    st.session_state.history_excel = excel_buffer.getvalue()
                    st.success("✅ Excel ready for download!")
                except ImportError:
                    st.error("❌ openpyxl not installed. Run: pip install openpyxl")
        
        with col3:
            pass
        
        st.markdown("---")
        
        # Download buttons - Only show if data is prepared
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.history_csv is not None:
                st.download_button(
                    label="📥 Download CSV",
                    data=st.session_state.history_csv,
                    file_name=f"parking_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("Click 'Prepare CSV Export' first")
        
        with col2:
            if st.session_state.history_excel is not None:
                st.download_button(
                    label="📊 Download Excel",
                    data=st.session_state.history_excel,
                    file_name=f"parking_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            else:
                st.info("Click 'Prepare Excel Export' first")
    
    else:
        st.info("📋 No parking history records yet")

# ============================================================================
# PAGE: ANALYTICS
# ============================================================================

elif page == "📈 Analytics":
    st.title("📊 Parking Analytics & Insights")
    
    # Get statistics
    stats = st.session_state.occupancy_tracker.get_statistics('day')
    
    # ===== KEY METRICS SECTION =====
    st.markdown("### 📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🚗 Total Vehicles", stats['total_vehicles'])
    with col2:
        st.metric("⏱️ Avg Duration", f"{stats['avg_duration']:.1f} min" if stats['avg_duration'] else "N/A")
    with col3:
        occupancy_status = st.session_state.parking_layout.get_occupancy_status()
        st.metric("🅿️ Occupancy", f"{occupancy_status['occupancy_rate']:.1f}%")
    with col4:
        # Calculate estimated revenue
        total_revenue = 0
        for entry in st.session_state.occupancy_tracker.history:
            if entry['exit_time']:
                duration_hours = (datetime.fromisoformat(entry['exit_time']) - 
                                datetime.fromisoformat(entry['entry_time'])).total_seconds() / 3600
                fee = max(100, round(duration_hours * 100, 2))
                total_revenue += fee
        st.metric("💰 Est. Revenue", f"Ksh.{total_revenue:.0f}")
    
    st.markdown("---")
    
    # ===== OPERATIONAL VISUALIZATIONS =====
    st.markdown("### 📈 Operational Analytics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚙 Vehicles by Spot Type")
        type_stats = stats['by_type']
        types = list(type_stats.keys())
        counts = [type_stats[t]['count'] for t in types]
        
        fig = go.Figure(
            data=[go.Bar(x=[t.title() for t in types], y=counts, marker_color='#1976D2')]
        )
        fig.update_layout(height=400, plot_bgcolor='#f8f9fa', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🅿️ Spot Occupancy Distribution")
        fig = create_occupancy_chart()
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ===== FINANCIAL ANALYTICS SECTION =====
    st.markdown("### 💰 Financial Analytics")
    
    # Calculate financial metrics
    revenue_by_type = {'standard': 0, 'handicap': 0, 'premium': 0}
    vehicles_exited = {'standard': 0, 'handicap': 0, 'premium': 0}
    duration_by_type = {'standard': 0, 'handicap': 0, 'premium': 0}
    
    for entry in st.session_state.occupancy_tracker.history:
        if entry['exit_time']:
            spot_type = entry['spot_type']
            duration_hours = (datetime.fromisoformat(entry['exit_time']) - 
                            datetime.fromisoformat(entry['entry_time'])).total_seconds() / 3600
            fee = max(100, round(duration_hours * 100, 2))
            
            revenue_by_type[spot_type] += fee
            vehicles_exited[spot_type] += 1
            duration_by_type[spot_type] += duration_hours
    
    # Financial metrics
    col1, col2, col3 = st.columns(3)
    
    total_revenue = sum(revenue_by_type.values())
    total_exited = sum(vehicles_exited.values())
    
    with col1:
        st.markdown(f"""
        <div class="info-card">
            💵 <b>Total Revenue</b><br>
            <p style='font-size: 2em; margin: 10px 0; font-weight: 700;'>Ksh.{total_revenue:.0f}</p>
            <small>{total_exited} vehicles</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_fee = total_revenue / total_exited if total_exited > 0 else 0
        st.markdown(f"""
        <div class="success-card">
            💳 <b>Average Fee</b><br>
            <p style='font-size: 2em; margin: 10px 0; font-weight: 700;'>Ksh.{avg_fee:.0f}</p>
            <small>per vehicle</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_duration_all = sum(duration_by_type.values()) / total_exited if total_exited > 0 else 0
        st.markdown(f"""
        <div class="warning-card">
            ⏱️ <b>Avg Parking Time</b><br>
            <p style='font-size: 2em; margin: 10px 0; font-weight: 700;'>{avg_duration_all:.2f} hrs</p>
            <small>average duration</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== REVENUE VISUALIZATIONS =====
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Revenue by Spot Type")
        revenue_types = [t.title() for t in revenue_by_type.keys()]
        revenue_amounts = list(revenue_by_type.values())
        
        fig = go.Figure(data=[
            go.Bar(
                x=revenue_types,
                y=revenue_amounts,
                marker_color=['#1976D2', '#87CEEB', '#FFD700'],
                text=[f'Ksh.{v:.0f}' for v in revenue_amounts],
                textposition='outside'
            )
        ])
        fig.update_layout(
            height=400,
            plot_bgcolor='#f8f9fa',
            yaxis_title='Revenue (Ksh)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Revenue Distribution")
        colors_pie = ['#1976D2', '#87CEEB', '#FFD700']
        fig = go.Figure(data=[
            go.Pie(
                labels=[t.title() for t in revenue_by_type.keys()],
                values=list(revenue_by_type.values()),
                marker=dict(colors=colors_pie),
                textinfo='label+percent+value',
                hovertemplate='<b>%{label}</b><br>Revenue: Ksh.%{value:.0f}<br>%{percent}<extra></extra>'
            )
        ])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ===== DETAILED FINANCIAL TABLE =====
    st.subheader("📊 Revenue Breakdown by Spot Type")
    
    financial_data = []
    for spot_type in ['standard', 'handicap', 'premium']:
        avg_fee_type = revenue_by_type[spot_type] / vehicles_exited[spot_type] if vehicles_exited[spot_type] > 0 else 0
        avg_duration_type = duration_by_type[spot_type] / vehicles_exited[spot_type] if vehicles_exited[spot_type] > 0 else 0
        
        financial_data.append({
            'Spot Type': spot_type.title(),
            'Vehicles Exited': vehicles_exited[spot_type],
            'Total Revenue': f"Ksh.{revenue_by_type[spot_type]:.0f}",
            'Avg Fee': f"Ksh.{avg_fee_type:.0f}",
            'Avg Duration': f"{avg_duration_type:.2f} hrs"
        })
    
    financial_df = pd.DataFrame(financial_data)
    st.dataframe(financial_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # ===== OPERATIONAL STATISTICS TABLE =====
    st.subheader("📋 Operational Statistics")
    
    # Get current occupancy status for real-time data
    occupancy_status = st.session_state.parking_layout.get_occupancy_status()
    
    stats_data = []
    for spot_type in ['standard', 'handicap', 'premium']:
        type_info = occupancy_status['by_type'][spot_type]
        current = type_info['occupied']
        total = type_info['total']
        available = total - current
        occupancy_pct = (current / total * 100) if total > 0 else 0
        
        stats_data.append({
            'Type': spot_type.title(),
            'Current Vehicles': current,
            'Total Capacity': total,
            'Available': available,
            'Occupancy Rate': f"{occupancy_pct:.1f}%"
        })
    
    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)

# ============================================================================
# PAGE: SETTINGS
# ============================================================================

elif page == "⚙️ Settings":
    st.title("⚙️ System Settings & Configuration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔧 Parking System Configuration")
        
        status = st.session_state.parking_layout.get_occupancy_status()
        
        st.info(f"""
        **Current Parking Lot Status:**
        - Total Capacity: {status['total_spots']} spots
        - Standard Spots: {status['by_type']['standard']['total']}
        - Handicap Spots: {status['by_type']['handicap']['total']}
        - Premium Spots: {status['by_type']['premium']['total']}
        """)
        
        st.markdown("---")
        
        st.subheader("🔄 Manage Parking Lot")
        
        # Reset button with confirmation
        col_reset_1, col_reset_2 = st.columns([2, 1])
        with col_reset_1:
            reset_btn = st.button("🔄 Reset Parking Lot", use_container_width=True, key="reset_btn")
        with col_reset_2:
            reset_confirm = st.checkbox("Confirm", key="reset_confirm")
        
        if reset_btn and reset_confirm:
            st.session_state.parking_layout.create_realistic_layout()
            st.session_state.parking_layout.save_config()
            st.success("✅ Parking lot reset successfully!")
            st.rerun()
        
        st.markdown("---")
        
        st.subheader("📊 Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Clear History button with confirmation
            clear_btn = st.button("🗑️ Clear History", use_container_width=True, key="clear_history_btn")
            clear_confirm = st.checkbox("Confirm Delete", key="clear_history_confirm")
            
            if clear_btn and clear_confirm:
                st.session_state.occupancy_tracker.history = []
                st.session_state.occupancy_tracker.save_history()
                st.success("✅ History cleared successfully!")
                st.rerun()
        
        with col2:
            # Export Config button
            if st.button("💾 Export Config", use_container_width=True, key="export_config_btn"):
                config_json = json.dumps({
                    'spots': st.session_state.parking_layout.spots,
                    'timestamp': datetime.now().isoformat()
                }, indent=2, default=str)
                st.download_button(
                    label="📥 Download Config JSON",
                    data=config_json,
                    file_name=f"parking_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True,
                    key="download_config"
                )
    
    with col2:
        st.subheader("ℹ️ System Info")
        st.info(f"""
        **App Version:** {SYSTEM_STATUS['version']}
        **Status:** {SYSTEM_STATUS['status']}
        **Environment:** {SYSTEM_STATUS['environment']}
        **Support:** {SYSTEM_STATUS['support_email']}
        """)
        
        st.markdown("---")
        st.subheader("📋 Real-time Status")
        st.write(f"""
        - 🅿️ **Total Spots:** {status['total_spots']}
        - 📊 **Occupancy:** {status['occupancy_rate']:.1f}%
        - 🚗 **Occupied:** {status['occupied_spots']}
        - ✅ **Available:** {status['available_spots']}
        - 🕐 **Last Updated:** {datetime.now().strftime('%H:%M:%S')}
        """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #888;'>
    <small>🅿️ Smart Parking System v{SYSTEM_STATUS['version']} | Powered by Streamlit & Python | © 2025</small>
</div>
""", unsafe_allow_html=True)