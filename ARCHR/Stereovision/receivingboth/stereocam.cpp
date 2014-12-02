/*
* 
* Project ARCHR: Mannan Javid (mannanj90@gmail.com) 
* Patrick Early
* Eric Eide
* Martyna Bula
*
* Original Author: sagar
*
* Created on 10 September, 2012, 7:48 PM
* 
*/
 
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
using namespace cv;
using namespace std;
 
int main() {

int LHoriz = 0;
int RHoriz = 0;
int LVertical = 0;
int RVertical = 0;
//VideoCapture streamL("http://127.0.0.1:9090/camera.mjpg");   //0 is the id of video device.0 if you have only one camera.
//VideoCapture streamR("http://127.0.0.1:9091/camera.mjpg");   //0 is the id of video device.0 if you have only one camera. 
//for local stream /camera.mjpg is needed
VideoCapture streamL(1);             //0 is the id of video device.0 if you have only one camera.
VideoCapture streamR(0);             //0 is the id of video device.0 if you have only one camera.

if (!streamL.isOpened()) {           //check if video device has been initialised
cout << "cannot open camera";
}
 
if (!streamR.isOpened()) {          
cout << "cannot open camera";
}
 

//unconditional loop
while (true) {
Mat cameraFrameL, resizedFrameL;
Mat cameraFrameR, resizedFrameR;
Mat Stereo, roi;                    //for Stereo combination
Stereo = Mat(Size(1280, 700), CV_8UC3);   //img type CV_8UC3 corresponds to if gray?              
Mat edges;                          //for filters

//Read Camera Frames
streamL.read(cameraFrameL);
streamR.read(cameraFrameR);
LHoriz = 320;
RHoriz = 320;
LVertical = 240;
RVertical = 240;
resize(cameraFrameL, resizedFrameL, Size(LHoriz, LVertical), 0, 0, INTER_CUBIC);
resize(cameraFrameR, resizedFrameR, Size(RHoriz, RVertical), 0, 0, INTER_CUBIC);

//Convert from gray back to color
//cvtColor(cameraFrameR, color, COLOR_GRAY2BGR);
//cvCvtColor(frame, gray, CV_BGR2GRAY);
//cvtColor(cameraFrameR, cameraFrameR, CV_GRAY2RGB);

//Shows Left and Right Frames separately
//imshow("camL", cameraFrameL);     //originals
//imshow("camR", cameraFrameR);
//imshow("Left", resizedFrameL);      //resized to oculus dimensions
//imshow("Right", resizedFrameR);     //each eye is 640x800 (1280x800 total)


//Combines the two frames into one Stereo image using Mats and copyTo
roi = Mat(Stereo, Rect(170, 240, LHoriz, LVertical));        //places it top left
resizedFrameL.copyTo(roi);
roi = Mat(Stereo, Rect(LHoriz+185+(650/3), 240, RHoriz, RVertical));      //places it top right
resizedFrameR.copyTo(roi);
imshow("Stereo", Stereo);
//imshow("left", cameraFrameL);
//("leftAgain", cameraFrameL);
//roi = Mat(Stereo, Rect(0, 240, 640, 240));    //bottom left
//resizedFrameR.copyTo(roi);
//roi = Mat(Stereo, Rect(320, 240, 320, 240));  //bottom right
//resizedFrameR.copyTo(roi);



//Filters below
/*Edge detection
cvtColor(resizedFrameL, edges, CV_BGR2GRAY);
GaussianBlur(edges, edges, Size(7,7), 1.5, 1.5);
Canny(edges, edges, 0, 30, 3);
imshow("edges", edges);*/

if (waitKey(30) >= 0)
break;
}
return 0;
}
