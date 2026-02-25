import cv2 
import numpy as np
import os 
import time
import glob


#-----Camera stuffs-------#
# Initialize the camera using OpenCV VideoCapture. 0 typically refers to the default camera.
cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)
cap3 = cv2.VideoCapture(3)
                        
if not cap0.isOpened():
    print("Error: Could not open video device 0.")
    exit()
elif not cap1.isOpened():
    print("Error: Could not open video device 1.")
    exit()
elif not cap2.isOpened():
    print("Error: Could not open video device 2.")
    exit()
elif not cap3.isOpened():
    print("Error: Could not open video device 3.")
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
            for i in range(3): #capture image 
                  ret0, frame0 = cap0.read() # Read a frame from the camera
                  ret1, frame1 = cap1.read()
                  ret2, frame2 = cap2.read()
                  ret3, frame3 = cap3.read()
                                    
                  #cv2.imshow('image',frame)
                  if ret0:
                      # Save the captured frame as a PNG file
                      cv2.imwrite(f"{folder}/cam1_frame_{i}.png", frame0)
                      print(f"Captured cam 1 frame_{i}.png")
                  if ret1:
                      # Save the captured frame as a PNG file
                      cv2.imwrite(f"{folder}/cam2_frame_{i}.png", frame1)
                      print(f"Captured cam 2 frame_{i}.png")
                  if ret2:
                      # Save the captured frame as a PNG file
                      cv2.imwrite(f"{folder}/cam3_frame_{i}.png", frame2)
                      print(f"Captured cam 3 frame_{i}.png")
                  if ret3:
                      # Save the captured frame as a PNG file

                      cv2.imwrite(f"{folder}/cam4_frame_{i}.png", frame3)
                      print(f"Captured cam 4 frame_{i}.png")
                      
                      
                      
                    
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



cap0.release()
cap1.release()
cap2.release()
cap3.release()
cv2.destroyAllWindows()