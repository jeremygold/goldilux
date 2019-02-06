#!/usr/bin/env bash

# FIXME - bring these back for full script
# sudo apt update
# sudo apt -y upgrade
# sudo apt -y autoremove

sudo apt -y install cmake libudev0 libudev-dev freeglut3 freeglut3-dev libxmu6 libxmu-dev libxi6 libxi-dev

################################################################################
##### Install Processing #####
if [ ! -f /usr/local/bin/processing ]; then
  curl https://processing.org/download/install-arm.sh | sudo sh
else
  echo "Processing already installed"
fi

################################################################################
##### Clone, build, and install libusb #####
sudo apt -y install autotools-dev autoconf libtool libudev-dev
cd ~
if [ ! -d libusb ]; then
  git clone https://github.com/libusb/libusb.git
else
  echo "libusb already cloned"
fi

cd libusb
./autogen.sh
make && sudo make install

################################################################################
##### Clone, build, and install libfreenect #####
cd ~
if [ ! -d libfreenect ]; then
  git clone https://github.com/OpenKinect/libfreenect.git
else
  echo "libfreenect already cloned"
fi

cd libfreenect
mkdir -p build
cd build
cmake -L \
	-DLIBUSB_1_INCLUDE_DIR=/home/pi/libusb/libusb/ \
	-DLIBUSB_1_LIBRARY=/usr/local/lib/libusb-1.0.so \
	-DBUILD_OPENNI2_DRIVER=ON \
	-DBUILD_PYTHON3=ON \
	..
make && sudo make install

wget https://github.com/OpenKinect/libfreenect/blob/master/platform/linux/udev/51-kinect.rules
sudo mv 51-kinect.rules /etc/udev/rules.d/

