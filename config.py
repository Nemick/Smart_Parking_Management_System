"""
Smart Parking System - Configuration Module
Centralized configuration for the entire system
"""

# ============================================================================
# PARKING LOT CONFIGURATION
# ============================================================================

PARKING_LOT_CONFIG = {
    'name': 'Downtown Smart Parking Lot',
    'total_capacity': 32,
    'rows': 4,
    'spots_per_row': 8,
    'address': '123 Main Street',
    'phone': '+1-555-PARKING',
    'email': 'info@smartparking.com'
}

# Spot type distribution
SPOT_DISTRIBUTION = {
    'standard': 28,    # General parking
    'handicap': 2,     # Accessible spots (spots 1-2)
    'premium': 2       # VIP/Priority spots (spots 31-32)
}

# ============================================================================
# PRICING CONFIGURATION
# ============================================================================

PRICING = {
    'base_rate_per_hour': 100.00,
    'minimum_charge': 100.00,
    'currency': 'Ksh.',
    'discount': {
        'handicap': 0.50,      # 50% discount
        'long_stay': 0.10,     # 10% after 4 hours
        'monthly_pass': 50.00  # Monthly subscription
    }
}

# ============================================================================
# LICENSE PLATE DETECTION CONFIG
# ============================================================================

DETECTION_CONFIG = {
    'model_path': 'trained_license_plate_detector.pt',
    'confidence_threshold': 0.25,
    'ocr_language': 'en',
    'image_preprocessing': {
        'grayscale': True,
        'histogram_equalization': True,
        'upscale_factor': 2,
        'min_image_size': (320, 320),
        'max_image_size': (1920, 1920)
    },
    'supported_formats': ['jpg', 'jpeg', 'png', 'bmp', 'tiff']
}

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DATABASE_CONFIG = {
    'parking_config_file': 'parking_config.json',
    'history_file': 'parking_history.json',
    'records_file': 'parking_records.csv',
    'backup_enabled': True,
    'backup_interval': 3600  # seconds (1 hour)
}

# ============================================================================
# STREAMLIT UI CONFIGURATION
# ============================================================================

UI_CONFIG = {
    'theme': 'light',
    'sidebar_state': 'expanded',
    'layout': 'wide',
    'title': '🅿️ Smart Parking System',
    'logo': '🅿️',
    'colors': {
        'occupied': '#FF6B6B',
        'available_standard': '#90EE90',
        'available_handicap': '#87CEEB',
        'available_premium': '#FFD700',
        'empty': '#CCCCCC',
        'primary': '#1f77b4'
    },
    'sidebar_stats': {
        'show_total_spots': True,
        'show_occupied': True,
        'show_available': True,
        'show_occupancy_pct': True
    }
}

# ============================================================================
# NOTIFICATION CONFIGURATION
# ============================================================================

NOTIFICATIONS = {
    'enabled': True,
    'email_alerts': False,
    'sms_alerts': False,
    'in_app_alerts': True,
    'alert_rules': {
        'lot_full': True,
        'long_stay': True,
        'duration_hours': 4
    }
}

# ============================================================================
# ANALYTICS CONFIGURATION
# ============================================================================

ANALYTICS_CONFIG = {
    'enabled': True,
    'track_peak_hours': True,
    'track_revenue': True,
    'prediction_enabled': False,
    'retention_days': 90
}

# ============================================================================
# SECURITY CONFIGURATION
# ============================================================================

SECURITY_CONFIG = {
    'require_authentication': False,
    'data_encryption': False,
    'backup_encryption': False,
    'audit_logs': False,
    'password_protected_settings': False
}

# ============================================================================
# PERFORMANCE CONFIGURATION
# ============================================================================

PERFORMANCE_CONFIG = {
    'cache_enabled': True,
    'cache_ttl_seconds': 300,  # 5 minutes
    'lazy_load_images': True,
    'gpu_acceleration': True,
    'batch_processing': False,
    'max_concurrent_uploads': 5
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': 'parking_system.log',
    'max_file_size': 10485760,  # 10 MB
    'backup_count': 5
}

# ============================================================================
# API CONFIGURATION (Future Use)
# ============================================================================

API_CONFIG = {
    'enabled': False,
    'host': '0.0.0.0',
    'port': 5000,
    'debug': False,
    'cors_enabled': True,
    'rate_limit': 1000,
    'api_version': '1.2.0'
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_config(section, key=None):
    """Get configuration value"""
    configs = {
        'parking_lot': PARKING_LOT_CONFIG,
        'pricing': PRICING,
        'detection': DETECTION_CONFIG,
        'database': DATABASE_CONFIG,
        'ui': UI_CONFIG,
        'notifications': NOTIFICATIONS,
        'analytics': ANALYTICS_CONFIG,
        'security': SECURITY_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'logging': LOGGING_CONFIG,
        'api': API_CONFIG
    }
    
    if section not in configs:
        raise ValueError(f"Unknown configuration section: {section}")
    
    if key:
        return configs[section].get(key)
    else:
        return configs[section]

def update_config(section, key, value):
    """Update configuration value"""
    configs = {
        'parking_lot': PARKING_LOT_CONFIG,
        'pricing': PRICING,
        'detection': DETECTION_CONFIG,
        'database': DATABASE_CONFIG,
        'ui': UI_CONFIG,
        'notifications': NOTIFICATIONS,
        'analytics': ANALYTICS_CONFIG,
        'security': SECURITY_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'logging': LOGGING_CONFIG,
        'api': API_CONFIG
    }
    
    if section in configs:
        configs[section][key] = value
        return True
    return False

# ============================================================================
# SYSTEM STATUS
# ============================================================================

SYSTEM_STATUS = {
    'version': '1.2.0',
    'status': 'ACTIVE',
    'last_updated': '2025-11-16',
    'environment': 'PRODUCTION',
    'support_email': 'support@smartparking.com'
}
