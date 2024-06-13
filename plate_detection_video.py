import cv2
import pytesseract
import openpyxl
import os

# Define the width and height of the video frames
width = 640
height = 480

# Initialize the row index from 2
excel_row = 2
url = 'http://192.168.29.43:8080/video'
# Load the Haar cascade classifier for license plate detection
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

# Open the video file
cap = cv2.VideoCapture(url)

# Create a new Excel workbook
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet["A1"] = "Image Path"
sheet["B1"] = "Detected Text"
sheet["C1"] = "Fine"

# Create a directory to store the images
image_dir = "detected_images"
os.makedirs(image_dir, exist_ok=True)

while True:
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        break  # Break the loop if no frame is read

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect license plates in the frame
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Iterate over the detected license plates
    for idx, (x, y, w, h) in enumerate(plates, start=2):  # Start from row 2
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Extract the detected license plate region
        plate_region = gray[y:y + h, x:x + w]

        # Use pytesseract to perform OCR on the grayscale image
        pytesseract.pytesseract.tesseract_cmd = r'E:\pythonProject\tesseract.exe'
        text = pytesseract.image_to_string(plate_region)

        # Save the extracted region image with detected text
        image_filename = os.path.join(image_dir, f"plate_{excel_row}.jpg")
        cv2.imwrite(image_filename, frame)

        # Write image path and detected text to Excel
        sheet[f"A{excel_row}"] = image_filename
        sheet[f"B{excel_row}"] = text
        sheet[f"C{excel_row}"] = "500"

        excel_row += 1

    # Display the frame with license plate detection
    cv2.imshow('Plate Detection', frame)

    # Check for 'q' key press to exit
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

# Save the Excel workbook
workbook.save("detected_text.xlsx")

# Release resources
workbook.close()
cap.release()
cv2.destroyAllWindows()
