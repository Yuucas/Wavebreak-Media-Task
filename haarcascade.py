import cv2
import numpy as np
import glob
from pathlib import Path
import os

# Find all image files in a directory
types = [".jpg", ".png", ".jpeg", ".avif", ".bmp", ".tiff"]
folder = Path("C:/Users/yukse/Desktop/Lectures/VSCode/Computer Vision/images_task1/")
image_files = sorted([path.as_posix() for path in filter(lambda path: path.suffix in types, folder.glob('*'))])

# We point OpenCV's CascadeClassifier function to where our 
# classifier (XML file format) is stored
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

for image_file in image_files:
    # Get the file names
    file_path = image_file
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Load our image then convert it to grayscale
    image = cv2.imread(image_file)
    width, height = image.shape[1], image.shape[0]    

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    width = int(width) * 0.05
    height = int(height) * 0.05
    
    # Our classifier returns the ROI of the detected face as a tuple
    # It stores the top left coordinate and the bottom right coordiantes
    faces = face_classifier.detectMultiScale(gray, scaleFactor = 1.10, minNeighbors = 10, minSize=(int(width), int(height)), flags=cv2.CASCADE_SCALE_IMAGE)


    # When no faces detected, face_classifier returns and empty tuple
    if faces is ():
       print("No faces found")
        
    # Create a folder to save the detected faces
    if not os.path.exists("detected_faces"):
        os.mkdir("detected_faces")

    # We iterate through our faces array and save faces that are found
    # over each face in faces
    for i, (x,y,w,h) in enumerate(faces):
        face = image[y:y+h, x:x+w]
        cv2.imwrite("detected_faces/{}_{}.jpg".format(file_name, i), face)
