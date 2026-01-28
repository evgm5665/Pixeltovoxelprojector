
from picamera2 import Picamera2, Preview
import time
import numpy as np
import os
import glob

#-----Camera stuffs-------#
picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
#-----End of Camera stuffs-------#


#-----Varaibles-------#

folder = "/home/usl/modifly/PixtoVoxProject/motionimages"  #---motion images folder path
num = len(os.listdir(folder))                              #--- counts number of items in MI folder
folder_conts = os.listdir(folder)                          #--- returns a list of the items in MI folder

#-----End of Varaibles-------#


class Functions:
      #class created to hold find and delete dunctions and to keep track of shared variables
      #note to remember: to use variables : Functions.variable_name
 

      @staticmethod
      def Delete_Files():
            files_to_remove = glob.glob(os.path.join(folder, '*.png'))
            for item in folder_conts:
                  os.remove(files_to_remove.pop(0))     #removes png files 
                #  files_to_remove.pop()
            print("images deleted")    
            return 0  
      
      @staticmethod
      def Take_Pictures():
            for i in range(4): #capture image 
                  picam2.capture_file(f"{folder}/frame_00{i}.png")
                  time.sleep(1)
            print("images captured")
         

#-----End of class definitions -------#




###_______________Start of Program_____________________###


print("checking motion folder amt..")
            

      ###_____________Check motion folder amt _____________________###
if num < 5:

      print("Capturing images..>")

            ###______________Cam Start _____________________###

       
      picam2.start()
      time.sleep(0.5)
 

            ###______________Capture Images _____________________###

      Functions.Take_Pictures()

      print("Sending images to motionimages..")
            
      
      picam2.stop()

      
elif num >= 5:

      print("MI is full, deleting images..")

      Functions.Delete_Files()

      print("items deleted")
