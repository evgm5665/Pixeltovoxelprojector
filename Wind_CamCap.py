Wind_CampCap.py

import cv2 
import numpy as np
import os 
import time
import glob

#-----Camera stuffs-------#
# Initialize the camera using OpenCV VideoCapture. 0 typically refers to the default camera.
cap = cv2.VideoCapture(1,2,3)
 
if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()




#-----End of Camera stuffs-------#


#-----Varaibles-------#

folder = "motionimages"  #---motion images folder path

# Ensure the directory exists
if not os.path.exists(folder):
    os.makedirs(folder)

num = len(os.listdir(folder))                              #--- counts number of items in MI folder
folder_conts = os.listdir(folder)                          #--- returns a list of the items in MI folder


class Functions:
      #class created to hold find and delete functions and to keep track of shared variables
      #note to remember: to use variables : Functions.variable_name
 
      @staticmethod
      def Delete_Files():
            files_to_remove = glob.glob(os.path.join(folder, '*.png'))
            for filepath in files_to_remove:
                  os.remove(filepath)     #removes png files 
            print("images deleted")    
            
            global num, folder_conts
            num = len(os.listdir(folder))
            folder_conts = os.listdir(folder)
            return 0  
      
      @staticmethod
      def Take_Pictures():
            for i in range(4): #capture image 
                  ret, frame = cap.read() # Read a frame from the camera
                  cv2.imshow('image',frame)
                  if ret:
                      # Save the captured frame as a PNG file
                      cv2.imwrite(f"{folder}/frame_00{i}.png", frame)
                      print(f"Captured frame_00{i}.png")
                  else:
                      print(f"Failed to capture frame {i}")
                  time.sleep(1)
            print("images captured")
            
            global num, folder_conts
            num = len(os.listdir(folder))
            folder_conts = os.listdir(folder)
         

#-----End of class definitions -------#


###_______________Start of Program_____________________###

print("checking motion folder amt..")
            

###_____________Check motion folder amt _____________________###
if num < 5:

      print("Capturing images..>")

      ###______________Cam Start / Capture Images _____________________###
      # With OpenCV VideoCapture, the device is opened once at the start of the script.
      
      Functions.Take_Pictures()

      print("Sending images to motionimages..")
            
      
      
elif num >= 5:

      print("MI is full, deleting images first..>")
      Functions.Delete_Files()
      print("Starting capture now..>")
      Functions.Take_Pictures()



cap.release()
cv2.destroyAllWindows()