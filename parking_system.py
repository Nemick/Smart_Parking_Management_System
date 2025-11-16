import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button

# Parking Layout Class
class ParkingLayout:
    def __init__(self, config_file='parking_config.json'):
        """
        Initialize parking layout matching real-world parking lot structure.
        Layout: Two rows of spots facing each other with a driving lane between them.
        """
        self.config_file = config_file
        self.spots = {}
        self.load_or_create_config()
    
    def load_or_create_config(self):
        """Load existing config or create realistic default layout"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.spots = {int(k): v for k, v in config['spots'].items()}
                
                # Check if config has new format with 'row' key
                if self.spots and 'row' not in list(self.spots.values())[0]:
                    print("Old config format detected. Creating new layout...")
                    self.create_realistic_layout()
                    self.save_config()
        except FileNotFoundError:
            self.create_realistic_layout()
            self.save_config()
    
    def create_realistic_layout(self):
        """Create parking layout matching the uploaded image"""
        spot_id = 1
        
        # Row 1 (Top): 8 spots facing down toward driving lane
        for col in range(8):
            spot_type = 'handicap' if col < 2 else 'standard'
            self.spots[spot_id] = {
                'row': 1,
                'position': col + 1,
                'side': 'north',
                'type': spot_type,
                'occupied': False,
                'vehicle_info': None,
                'entry_time': None
            }
            spot_id += 1
        
        # Row 2 (Below Row 1): 8 spots facing up toward driving lane
        for col in range(8):
            self.spots[spot_id] = {
                'row': 2,
                'position': col + 1,
                'side': 'south',
                'type': 'standard',
                'occupied': False,
                'vehicle_info': None,
                'entry_time': None
            }
            spot_id += 1
        
        # Row 3 (Middle section): 8 spots facing down
        for col in range(8):
            self.spots[spot_id] = {
                'row': 3,
                'position': col + 1,
                'side': 'north',
                'type': 'standard',
                'occupied': False,
                'vehicle_info': None,
                'entry_time': None
            }
            spot_id += 1
        
        # Row 4 (Below Row 3): 8 spots facing up
        for col in range(8):
            spot_type = 'premium' if col >= 6 else 'standard'
            self.spots[spot_id] = {
                'row': 4,
                'position': col + 1,
                'side': 'south',
                'type': spot_type,
                'occupied': False,
                'vehicle_info': None,
                'entry_time': None
            }
            spot_id += 1
    
    def save_config(self):
        """Save current configuration to file"""
        config = {'spots': self.spots}
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    def get_spot_info(self, spot_id):
        """Get information about a specific spot"""
        return self.spots.get(spot_id)
    
    def get_available_spots(self, spot_type=None):
        """Get list of available spots, optionally filtered by type"""
        return [
            spot_id for spot_id, spot in self.spots.items()
            if not spot['occupied'] and (spot_type is None or spot['type'] == spot_type)
        ]
    
    def occupy_spot(self, spot_id, vehicle_info):
        """Mark a spot as occupied with vehicle information"""
        if spot_id not in self.spots or self.spots[spot_id]['occupied']:
            return False
        
        self.spots[spot_id].update({
            'occupied': True,
            'vehicle_info': vehicle_info,
            'entry_time': datetime.now().isoformat()
        })
        self.save_config()
        return True
    
    def release_spot(self, spot_id):
        """Mark a spot as available"""
        if spot_id not in self.spots or not self.spots[spot_id]['occupied']:
            return False
        
        self.spots[spot_id].update({
            'occupied': False,
            'vehicle_info': None,
            'entry_time': None
        })
        self.save_config()
        return True
    
    def get_occupancy_status(self):
        """Get current occupancy statistics"""
        total = len(self.spots)
        occupied = sum(1 for spot in self.spots.values() if spot['occupied'])
        by_type = {
            spot_type: {
                'total': sum(1 for spot in self.spots.values() if spot['type'] == spot_type),
                'occupied': sum(1 for spot in self.spots.values() 
                              if spot['type'] == spot_type and spot['occupied'])
            }
            for spot_type in ['standard', 'handicap', 'premium']
        }
        
        return {
            'total_spots': total,
            'occupied_spots': occupied,
            'available_spots': total - occupied,
            'occupancy_rate': (occupied / total * 100) if total > 0 else 0,
            'by_type': by_type
        }

# Create parking layout instance
parking_layout = ParkingLayout()

# Parking Visualizer Class - Interactive Visualization
class ParkingVisualizer:
    def __init__(self, parking_layout):
        self.parking_layout = parking_layout
        self.selected_spot = None
        self.fig = None
        self.ax = None
    
    def draw_parking_lot(self):
        """Draw interactive parking lot visualization"""
        if self.fig is not None:
            plt.close(self.fig)
        
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.ax.set_xlim(0, 20)
        self.ax.set_ylim(0, 12)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.selected_spot = None
        
        # Title
        self.ax.text(10, 11, 'PARKING LOT', ha='center', va='center', 
                    fontsize=16, fontweight='bold')
        
        # Define spot dimensions
        spot_width = 2
        spot_height = 1.5
        lane_width = 1.5
        
        # Color scheme
        colors = {
            'standard': '#90EE90',      # Light green
            'handicap': '#87CEEB',      # Sky blue
            'premium': '#FFD700',       # Gold
            'occupied': '#FF6B6B'       # Red
        }
        
        # Draw parking spots by row
        y_positions = {
            1: 9,      # Top row
            2: 7,      # Below top row
            3: 4.5,    # Middle row
            4: 2.5     # Bottom row
        }
        
        spot_rectangles = {}
        
        for spot_id, spot in self.parking_layout.spots.items():
            row = spot['row']
            col = spot['position'] - 1
            
            # Calculate position
            x = 1 + col * spot_width
            y = y_positions[row]
            
            # Determine color
            if spot['occupied']:
                color = colors['occupied']
            else:
                color = colors[spot['type']]
            
            # Draw rectangle
            rect = patches.Rectangle((x, y), spot_width, spot_height,
                                    linewidth=2, edgecolor='black',
                                    facecolor=color, alpha=0.7)
            self.ax.add_patch(rect)
            spot_rectangles[spot_id] = rect
            
            # Add spot ID
            self.ax.text(x + spot_width/2, y + spot_height/2, str(spot_id),
                        ha='center', va='center', fontsize=10, fontweight='bold')
            
            # Add type indicator
            type_label = ''
            if spot['type'] == 'handicap':
                type_label = '♿'
            elif spot['type'] == 'premium':
                type_label = '⭐'
            
            if type_label:
                self.ax.text(x + spot_width/2, y + spot_height - 0.3, type_label,
                           ha='center', va='center', fontsize=12)
            
            # Add license plate if occupied
            if spot['occupied'] and spot['vehicle_info']:
                license = spot['vehicle_info'].get('license_plate', 'N/A')
                self.ax.text(x + spot_width/2, y + 0.3, license,
                           ha='center', va='center', fontsize=8, 
                           color='white', fontweight='bold')
        
        # Draw driving lanes
        lane_y_positions = [7.8, 5.3]
        for lane_y in lane_y_positions:
            lane = patches.Rectangle((0.5, lane_y - lane_width/2), 18, lane_width,
                                    linewidth=1, edgecolor='gray',
                                    facecolor='#CCCCCC', alpha=0.3)
            self.ax.add_patch(lane)
        
        # Legend
        legend_x = 1
        legend_y = 0.5
        legend_items = [
            ('Available', colors['standard']),
            ('Occupied', colors['occupied']),
            ('Handicap', colors['handicap']),
            ('Premium', colors['premium'])
        ]
        
        for i, (label, color) in enumerate(legend_items):
            rect = patches.Rectangle((legend_x + i*3.5, legend_y), 0.5, 0.3,
                                    facecolor=color, edgecolor='black', alpha=0.7)
            self.ax.add_patch(rect)
            self.ax.text(legend_x + i*3.5 + 0.7, legend_y + 0.15, label,
                        va='center', fontsize=9)
        
        # Make spots clickable
        def on_click(event):
            if event.inaxes != self.ax:
                return
            
            # Find clicked spot
            for spot_id, spot in self.parking_layout.spots.items():
                row = spot['row']
                col = spot['position'] - 1
                x = 1 + col * spot_width
                y = y_positions[row]
                
                if (x <= event.xdata <= x + spot_width and 
                    y <= event.ydata <= y + spot_height):
                    if not spot['occupied']:
                        self.selected_spot = spot_id
                        print(f"Selected spot {spot_id}")
                        plt.close(self.fig)
                    else:
                        print(f"Spot {spot_id} is occupied")
                    return
        
        self.fig.canvas.mpl_connect('button_press_event', on_click)
        
        # Add Skip button
        ax_skip = plt.axes([0.8, 0.01, 0.15, 0.05])
        btn_skip = Button(ax_skip, 'Skip (Auto-assign)')
        
        def skip(event):
            print("Skipping manual selection...")
            plt.close(self.fig)
        
        btn_skip.on_clicked(skip)
        
        plt.tight_layout()
        plt.show()
        
        return self.selected_spot

# Spot Assigner Class - Automatic Spot Assignment   
class SpotAssigner:
    def __init__(self, parking_layout):
        self.parking_layout = parking_layout
    
    def auto_assign_spot(self, vehicle_info):
        """Automatically assign best available spot"""
        preferred_type = vehicle_info.get('preferred_type', 'standard')
        has_handicap_permit = vehicle_info.get('handicap_permit', False)
        
        # Priority 1: Handicap permit holders get handicap spots
        if has_handicap_permit:
            available = self.parking_layout.get_available_spots('handicap')
            if available:
                spot_id = available[0]
                self.parking_layout.occupy_spot(spot_id, vehicle_info)
                return spot_id
        
        # Priority 2: Try to get preferred type
        available = self.parking_layout.get_available_spots(preferred_type)
        if available:
            spot_id = available[0]
            self.parking_layout.occupy_spot(spot_id, vehicle_info)
            return spot_id
        
        # Priority 3: Get any available spot
        available = self.parking_layout.get_available_spots()
        if available:
            spot_id = available[0]
            self.parking_layout.occupy_spot(spot_id, vehicle_info)
            return spot_id
        
        return None

# Create spot assigner instance
spot_assigner = SpotAssigner(parking_layout)


# Occupancy Tracker Class - Historical Data and Statistics
class OccupancyTracker:
    def __init__(self, parking_layout, history_file='parking_history.json'):
        self.parking_layout = parking_layout
        self.history_file = history_file
        self.history = self.load_history()
    
    def load_history(self):
        """Load parking history from file"""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_history(self):
        """Save parking history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=4)
    
    def record_entry(self, spot_id, vehicle_info):
        """Record vehicle entry"""
        spot = self.parking_layout.get_spot_info(spot_id)
        entry = {
            'spot_id': spot_id,
            'spot_type': spot['type'],
            'vehicle_info': vehicle_info,
            'entry_time': spot['entry_time'],
            'exit_time': None
        }
        self.history.append(entry)
        self.save_history()
    
    def record_exit(self, spot_id):
        """Record vehicle exit"""
        spot = self.parking_layout.get_spot_info(spot_id)
        if spot and spot['vehicle_info']:
            license_plate = spot['vehicle_info'].get('license_plate')
            
            # Find and update the entry
            for entry in reversed(self.history):
                if (entry['spot_id'] == spot_id and 
                    entry['vehicle_info'].get('license_plate') == license_plate and
                    entry['exit_time'] is None):
                    entry['exit_time'] = datetime.now().isoformat()
                    self.save_history()
                    break
    
    def get_statistics(self, period='day'):
        """Get parking statistics for a time period"""
        now = datetime.now()
        
        if period == 'day':
            cutoff = now - timedelta(days=1)
        elif period == 'week':
            cutoff = now - timedelta(weeks=1)
        elif period == 'month':
            cutoff = now - timedelta(days=30)
        else:
            cutoff = datetime.min
        
        # Filter relevant entries
        relevant_entries = [
            e for e in self.history
            if datetime.fromisoformat(e['entry_time']) >= cutoff
        ]
        
        # Calculate statistics
        total_vehicles = len(relevant_entries)
        durations = []
        by_type = {}
        
        for entry in relevant_entries:
            spot_type = entry['spot_type']
            
            if spot_type not in by_type:
                by_type[spot_type] = {'count': 0, 'durations': []}
            
            by_type[spot_type]['count'] += 1
            
            if entry['exit_time']:
                entry_time = datetime.fromisoformat(entry['entry_time'])
                exit_time = datetime.fromisoformat(entry['exit_time'])
                duration = (exit_time - entry_time).total_seconds() / 60  # minutes
                durations.append(duration)
                by_type[spot_type]['durations'].append(duration)
        
        # Calculate averages
        avg_duration = sum(durations) / len(durations) if durations else None
        
        type_stats = {}
        for spot_type, data in by_type.items():
            type_stats[spot_type] = {
                'count': data['count'],
                'duration_minutes': sum(data['durations']) / len(data['durations']) 
                                   if data['durations'] else 0
            }
        
        return {
            'total_vehicles': total_vehicles,
            'avg_duration': avg_duration,
            'by_type': type_stats
        }

# Create tracker instance
occupancy_tracker = OccupancyTracker(parking_layout)


