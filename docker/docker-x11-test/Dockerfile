# FROM jjanzic/docker-python3-opencv
# FROM czentye/opencv-video-minimal
FROM dymat/opencv

RUN apt-get update \
  && apt-get install -y xterm 
        # && apt-get install -qqy \
        # x11-apps \
        # xterm 

ENV DISPLAY :0

WORKDIR /work

CMD python python_opencv_demo.py