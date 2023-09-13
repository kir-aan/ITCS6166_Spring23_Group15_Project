## CCN Project Group 15
### Team Members:
Srikar Chamarthy - 801317299

Aneela Gannarapu - 801312361

Aravind Pabbisetty - 801254719

Sai Kiran Reddy Bokka - 801283586

### Project Title:
Video Call Application (WebRTC) with audio driven talking head generation.

### Introduction:
The project is centered around a video call, where we capture the audio of the caller (sender) and transmit over to the receiver where the face of the caller is transitioned to the animated character or a hero. While the audio of the caller remains the same. 

The key benefits of above transition are as follows:
* The privacy of the callers is protected as we are changing the face of callers to well-know characters. Thereby, the identity of users can be withheld with utmost security. 
* The disturbances that occur due to poor network connection can be avoided as we are transmitting only audio. This is because audio transmission requires less bandwidth when compared video transmission.

### Architecture:
We are planning to build a web application so we will be using Client-Server Architecture. We will be using WebRTC protocol for real time communication. In this application architecture first the peers will exchange their offer and anwser responses via a Signaling server.The offer and answer responses will contain session description, peers media capabilities etc. Once its done then they exchance ICE(Inter Connectivity Establishment) candidates to identify and exchange network adresses,ports via the same signaling server. In between the peers there will be a relay server which hosts the ML model used to convert the audio stream from the first peer using the face selected into the audio driven face stream. The relay server will send the converted stream to the other peer in the WebRTC session. The signaling server and relay server can be implemented using the same server but for the architecture purpose we have shown differently.
![Video Chat Application with Audio driven face](https://user-images.githubusercontent.com/28972981/220796088-b1e02861-2120-4e0b-a953-db1e09c13bf0.png)

### Requirements To run Audio Driven Talking Head
(This application can be used to record the audio and convert it into a talking head)
- Python environment 3.10.9
```
conda create -n makeittalk_env python=3.10.9
conda activate makeittalk_env
```
- Intall ffmpeg from here https://ffmpeg.org/download.html and the path to the environment variables.
- python packages
```
pip install -r requirements.txt
```
Note: If you get any building wheels error in the above step install visual studio and its c++ build tools 

- Download the following pre-trained models to `examples/ckpt` folder(as these files are large we are unable to push it to github)

| Model |  Link to the model | 
| :-------------: | :---------------: |
| Voice Conversion  | [Link](https://drive.google.com/file/d/1ZiwPp_h62LtjU0DwpelLUoodKPR85K7x/view?usp=sharing)  |
| Speech Content Module  | [Link](https://drive.google.com/file/d/1r3bfEvTVl6pCNw5xwUhEglwDHjWtAqQp/view?usp=sharing)  |
| Speaker-aware Module  | [Link](https://drive.google.com/file/d/1rV0jkyDqPW-aDJcj7xSO6Zt1zSXqn1mu/view?usp=sharing)  |
| Image2Image Translation Module  | [Link](https://drive.google.com/file/d/1i2LJXKp-yWKIEEgJ7C6cE3_2NirfY_0a/view?usp=sharing)  |
| Non-photorealistic Warping (.exe)  | [Link](https://drive.google.com/file/d/1rlj0PAUMdX8TLuywsn6ds_G6L63nAu0P/view?usp=sharing)  |

- To run the audiorecord.py use the below command:
```
streamlit run audiorecord.py
```
- Open the browser and select an image in the side bar and record audio by clicking on start once you click on stop the model will process the audio will show a talking head video on the browser.

### Requirements To run real time face swap using mediapipe model.
(This is a real time video call application where user is able to swap their face with the selected image)
- Python environment 3.10.9 
```
conda create -n realtime python=3.10.9
conda activate realtime
```
- python packages
```
pip install -r requirements.txt
```
- Change the directory to Real_Time_Face_Swap
```
cd Real_Time_Face_Swap
```
- To run the realtime_faceswap.py use the below command
```
streamlit run realtime_faceswap.py
```
Note: To start the video call with 2 clients in same system open the same url in another browser window. Select an image and start the video call. To start the video call with 2 clients from different systems connect to the same network and run the application. Now add the application network url to chrome flags Insecure origins treated as secure in the two systems. 
![image](https://user-images.githubusercontent.com/112770055/235764802-7bd68e57-a63f-49ba-91b0-af6212afce08.png)

You can also choose to convert the face into a cartoon from the sidebar options instead of face swap. 

### Iteration 1:
* Installing Python3.x
* Installing Conda and setting up Conda environment.
* Researching provided ML models for the audio driven approach and deciding which model to implement.
* Learning about streamlit and WebRTC concepts.

### Iteration 2:
* Creating a UI design for the application.
* Developing a video call application using WebRTC(aiortc library).
* Implementing code to send the audio stream and the image selected in the UI to the relay server.

### Iteration 3:
* Installing all the required libraries for the chosen ML model in the Conda environment.
* Integrating ML model to transform audio and selected image to generate a video.
* Transmitting the generated video to the second client via the relay server.

### Iteration 4:
* Developed a Real Time Face Swap application using the media pipe model.
* Testing the application end-to-end and checking the performance/latency of the application.
* Improve the code to optimize and improve lantency if needed.

### Iteration 5:
* Perform final tests to ensure the video transmission is in place and  work on fixing the bugs if any.
* Focus will be on the project documentation that includes step-by-step instructions to execute the project and presentations that includes test-case results.


![flowchart](https://user-images.githubusercontent.com/28972981/220804654-d224f40a-0608-4aa9-961b-52e3530f04eb.jpeg)
