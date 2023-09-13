#Video Call Application

#Import the required packages
import streamlit as st
from streamlit_server_state import server_state, server_state_lock
from streamlit_webrtc import WebRtcMode, webrtc_streamer, VideoProcessorBase, RTCConfiguration
from streamlit_image_select import image_select
import threading
import warnings
warnings.filterwarnings("ignore")
import cv2
import numpy as np
import av

from common import media_utils
import torch

device = "cpu"
model = torch.hub.load("bryandlee/animegan2-pytorch:main", "generator", device=device).eval()
face2paint = torch.hub.load("bryandlee/animegan2-pytorch:main", "face2paint", device=device)

width = 640
height = 480
src_image_paths = [
    "images/bill_gates.jpg",
    "images/steve_jobs.jpg",
    "images/donald_trump.jpg",
    "images/dwayne_johnson.jpg",
    "images/will_smith.jpg",
    "images/psy.jpg",
    "images/seok_koo_son.jpg",
    "images/hae_jin_yoo.jpg",
    "images/hyun_bin.png",
    "images/danial_henney.jpg",
]

src_images = []
for image_path in src_image_paths:
    image = cv2.imread(image_path)
    src_images.append(image)




st.title("Video Call Application")

#Main Function
def main():
    style_list = ['Face Swap', 'Cartoon']
    with st.sidebar:
        st.sidebar.header('Style Selection')
        style_selection = st.sidebar.selectbox("Choose your style:", style_list)
        src_img_path = image_select(label="Choose a Talking Head", 
        images=[
        "images/bill_gates.jpg",
        "images/steve_jobs.jpg",
        "images/donald_trump.jpg",
        "images/dwayne_johnson.jpg",
        "images/will_smith.jpg",
        "images/psy.jpg",
        "images/seok_koo_son.jpg",
        "images/hae_jin_yoo.jpg",
        "images/hyun_bin.png",
        "images/danial_henney.jpg",
        ],
        captions=["Bill Gates", "Steve Jobs", "Donald Trump", "Dwayne","will smith", "psy", "seok koo son","hae jin yoo", "hyun bin", "danial henney"],
        )
        image=cv2.imread(src_img_path)



    def set_src_image(image):
        global src_image, src_image_gray, src_mask, src_landmark_points, src_np_points, src_convexHull, indexes_triangles
        src_image = image
        src_image_gray = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
        src_mask = np.zeros_like(src_image_gray)

        src_landmark_points = media_utils.get_landmark_points(src_image)
        src_np_points = np.array(src_landmark_points)
        src_convexHull = cv2.convexHull(src_np_points)
        cv2.fillConvexPoly(src_mask, src_convexHull, 255)

        indexes_triangles = media_utils.get_triangles(convexhull=src_convexHull,
                                                    landmarks_points=src_landmark_points,
                                                    np_points=src_np_points)

    if "webrtc_contexts" not in server_state:
        server_state["webrtc_contexts"] = []

    #Creates Columns
    column1,column2 = st.columns(2)

    with column1:
        #Client 1 video and audio streamer
        st.header("Client 1")
        selfStream = webrtc_streamer(
            key="self",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration={
                    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                },
            media_stream_constraints={"video": True, "audio": True},
            sendback_audio=False,
        )
    
    with server_state_lock["webrtc_contexts"]:
        rtc_session = server_state["webrtc_contexts"]
        if selfStream.state.playing and selfStream not in rtc_session:
            rtc_session.append(selfStream)
            server_state["webrtc_contexts"] = rtc_session
        elif not selfStream.state.playing and selfStream in rtc_session:
            rtc_session.remove(selfStream)
            server_state["webrtc_contexts"] = rtc_session

    streamActive = []
    for stream in rtc_session:
        if stream!=selfStream and stream.state.playing:
            streamActive.append(stream)

    class VideoProcessor(VideoProcessorBase):
        def __init__(self):
            self.model_lock = threading.Lock()
            self.style = style_list[0]

        def update_style(self, new_style):
            if self.style != new_style:
                with self.model_lock:
                    self.style = new_style


        def recv(self, frame):
            image_video = frame.to_ndarray(format="bgr24")
            #face Swap
            if self.style == style_list[0]:
                global src_image, src_image_gray, src_mask, src_landmark_points, src_np_points, src_convexHull, indexes_triangles
                set_src_image(image)
                dest_image = image_video
                dest_image = cv2.resize(dest_image, (640, 480))

                dest_image_gray = cv2.cvtColor(dest_image, cv2.COLOR_BGR2GRAY)

                dest_landmark_points = media_utils.get_landmark_points(dest_image)
                
                if dest_landmark_points is None:
                    return frame
                
                dest_np_points = np.array(dest_landmark_points)
                dest_convexHull = cv2.convexHull(dest_np_points)

                height, width, channels = dest_image.shape
                new_face = np.zeros((height, width, channels), np.uint8)

                # Triangulation of both faces
                for triangle_index in indexes_triangles:
                    # Triangulation of the first face
                    points, src_cropped_triangle, cropped_triangle_mask, _ = media_utils.triangulation(
                        triangle_index=triangle_index,
                        landmark_points=src_landmark_points,
                        img=src_image)

                    # Triangulation of second face
                    points2, _, dest_cropped_triangle_mask, rect = media_utils.triangulation(triangle_index=triangle_index,
                                                                                            landmark_points=dest_landmark_points)

                    # Warp triangles
                    warped_triangle = media_utils.warp_triangle(rect=rect, points1=points, points2=points2,
                                                                src_cropped_triangle=src_cropped_triangle,
                                                                dest_cropped_triangle_mask=dest_cropped_triangle_mask)

                    # Reconstructing destination face
                    media_utils.add_piece_of_new_face(new_face=new_face, rect=rect, warped_triangle=warped_triangle)

                # Face swapped (putting 1st face into 2nd face)
                # new_face = cv2.medianBlur(new_face, 3)
                result = media_utils.swap_new_face(dest_image=dest_image, dest_image_gray=dest_image_gray,
                                                dest_convexHull=dest_convexHull, new_face=new_face)

                result = cv2.medianBlur(result, 3)
                return av.VideoFrame.from_ndarray(result, format="bgr24")
            
            #Cartoon
            if self.style == style_list[1]:
                im_inp = frame.to_image()
                im_out = face2paint(model, im_inp, side_by_side=False)
                return av.VideoFrame.from_image(im_out)

    
    with column2:
        st.header("Client 2")
        for stream in streamActive:
            ctx=webrtc_streamer(
                key=str(id(stream)),
                mode=WebRtcMode.RECVONLY,
                rtc_configuration={
                        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                        },
                media_stream_constraints={
                        "video": True,
                        "audio": True,
                    },
                video_processor_factory=VideoProcessor,
                source_audio_track=stream.output_audio_track,
                source_video_track=stream.output_video_track,
                desired_playing_state=stream.state.playing,
            )
            if ctx.video_processor:
                ctx.video_transformer.update_style(style_selection)
            


if __name__ == "__main__":
    main()