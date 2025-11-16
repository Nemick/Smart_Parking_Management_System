from ultralytics import YOLO
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import cv2
import os
import easyocr


# Load YOLOv8 model for license plate detection
model = YOLO('trained_license_plate_detector.pt')

# Parking Manager Class
class ParkingManager:
    def __init__(self, csv_path='parking_records.csv'):
        self.csv_path = csv_path
        self.reader = easyocr.Reader(['en'])  # Initialize OCR for English
        
        # Create or load the CSV file
        try:
            self.df = pd.read_csv(csv_path)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=[
                'timestamp', 'license_plate', 'confidence',
                'vehicle_image', 'entry_time'
            ])
            self.save_records()
    
    def preprocess_plate_image(self, img):
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Enhance contrast
        img = cv2.equalizeHist(img)
        
        # Resize for better OCR
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        return img
    
    def read_license_plate(self, image, bbox):
        try:
            x, y, w, h = map(int, bbox)
            # Extract plate region
            plate_img = image[y:y+h, x:x+w]
            
            # Preprocess the image
            processed_img = self.preprocess_plate_image(plate_img)
            
            # Perform OCR
            results = self.reader.readtext(processed_img)
            
            if results:
                # Get the text with highest confidence
                text, conf = max(results, key=lambda x: x[2])[1:3]
                # Clean the text (remove spaces and special characters)
                text = ''.join(c for c in text if c.isalnum()).upper()
                return text, conf
            
            return None, 0.0
            
        except Exception as e:
            print(f"Error reading license plate: {e}")
            return None, 0.0
    
    def add_parking_record(self, license_plate, confidence, vehicle_image):
        # Add new record
        new_record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'license_plate': license_plate,
            'confidence': confidence,
            'vehicle_image': vehicle_image,
            'entry_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.df = pd.concat([self.df, pd.DataFrame([new_record])], ignore_index=True)
        self.save_records()
        print(f"Added parking record for: {license_plate}")
    
    def save_records(self):
        self.df.to_csv(self.csv_path, index=False)
    
    def get_records(self):
        return self.df

# Initialize parking manager
parking_manager = ParkingManager()

# Function to detect and read license plates from an image
def detect_and_read_plate(image_path):
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image from {image_path}")
        return
    
    # Detect license plates
    results = model.predict(image_path, conf=0.25)
    
    if not results:
        print("No license plates detected")
        return
    
    result = results[0]
    plates_found = False
    
    # Create a copy for visualization
    display_img = image.copy()
    
    # Process each detection
    for box in result.boxes:
        # Get box coordinates
        bbox = box.xyxy[0].cpu().numpy()  # get box coordinates in (top, left, bottom, right) format
        conf = float(box.conf[0])
        
        # Convert bbox format from (x1,y1,x2,y2) to (x,y,w,h)
        x1, y1, x2, y2 = map(int, bbox)
        bbox_xywh = [x1, y1, x2-x1, y2-y1]
        
        # Read the license plate text
        plate_text, ocr_conf = parking_manager.read_license_plate(image, bbox_xywh)
        
        if plate_text:
            plates_found = True
            # Add to parking records
            parking_manager.add_parking_record(plate_text, ocr_conf * conf, os.path.basename(image_path))
            
            # Draw on image
            cv2.rectangle(display_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(display_img, f"{plate_text} ({ocr_conf:.2f})",
                       (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,
                       0.9, (0, 255, 0), 2)
    
    # Display results
    if plates_found:
        plt.figure(figsize=(12, 8))
        plt.imshow(cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title('License Plate Detection and OCR')
        plt.show()
        
        # Display parking records
        print("\nCurrent Parking Records:")
        print(parking_manager.get_records())



# # Test the license plate detection and OCR system
# print("Testing license plate detection and OCR system...")

# # Test with sample image
# sample_image = 'behind_view.jpg'
# detect_and_read_plate(sample_image)

# # Display all parking records
# print("\nAll parking records:")
# print(parking_manager.get_records())