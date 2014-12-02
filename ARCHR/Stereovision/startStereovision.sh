#!/bin/sh
# Project ARCHR: Mannan Javid (mannanj90@gmail.com) 
# 		  		 Patrick Early
#          		 Eric Eide
#         	     Martyna Bula
cd /home/archr/projects/archr_Code/Baxter/Stereovision/streaming && gnome-terminal --tab --command "python left.py" #--tab -e "python right.py"   
echo "======Stream started. There should be 2 tabs open======"
echo "======The left stream, and the right stream=="
echo "======The text will show: get jpeg when the respective cam image is being received=="
sleep 5

cd /home/archr/projects/archr_Code/Baxter/Stereovision && gnome-terminal --tab --command "./StereoCam"   
echo "======Stream started. There should be 2 tabs open======"
echo "======The left stream, and the right stream=="
echo "======The text will show: get jpeg when the respective cam image is being received=="
