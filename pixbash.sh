#!/bin/bash 

#  unfortunately need sleep commands for code to work properly 
#  program is designed to check and capture images from picam, build ray voxel, 
#  and run voxelmotionviewer all in one go and continuously run to mimic real time results. 


cd /home/usl/modifly/PixtoVoxProject



#STEP one picam capture

   python3 PiCameraCapture.py > -n        #runs program without outputing output from program into terminal

   #STEP two check that the images are in motionimages folder
   if [ "$(ls -A /home/usl/modifly/PixtoVoxProject/motionimages)" ]; 
   then
      echo "motionimages folder not empty, proceeding to next STEP"
        python3 PiCameraCapture.py
   else
      echo "motionimages folder empty, repeating STEP one"
        python3 PiCameraCapture.py
   fi   

sleep 0.5

    #STEP three build ray voxel
    echo "building ray voxel.."
   ./build/ray_voxel motionimages/metadata.json motionimages voxel_grid.bin $?   1>> rayvoxel_log.txt 2>> rayvoxel_errlog.txt > -n #builds ray_voxel and logs output and errors
        echo "ray voxel build complete, checking for errors"

        #STEP four check for error
        if [ $? -eq 0 ]; then
           echo "no error detected, proceeding to next STEP"

        else
           echo "not detecting frames, exiting"
            exit 1
        fi  
sleep  2 
            #STEP five switch to venv
            source /home/usl/modifly/PixtoVoxProject/.venv/bin/activate $? > -n
            if [ $? -eq 0 ]; then
            echo "switched to venv, proceeding to next STEP"
            else
            echo "failed to switch to venv, exiting"
                exit 1
            fi
sleep 1
            #STEP six run voxelmotion.py
            python3 voxelmotionviewer.py $? > -n
            if [ $? -eq 0 ]; then
            echo "she aint working but she aint broke, all STEPs complete"
            else
            echo "voxelmotion.py failed, exiting"
                exit 1
            fi
