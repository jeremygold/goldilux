#!/usr/bin/env bash

# FIXME - bring these back for full script
# sudo apt update
# sudo apt -y upgrade
# sudo apt -y autoremove

################################################################################
##### Download and extract processing #####

processing_download=processing-3.5.3-linux-armv6hf.tgz

if [ ! -f processing-3.5.3/processing ]; then
  echo "Installing Processing"

  if [ ! -f $processing_download ]; then
    echo "Downloading $processing_download"
    wget http://download.processing.org/$processing_download
  else
    echo "Using cached download: $processing_download"
  fi

  tar xvzf $processing_download
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

sudo apt -y install cmake
cd ~
if [ ! -d libfreenect ]; then
  git clone https://github.com/OpenKinect/libfreenect.git
else
  echo "libfreenect already cloned"
fi

cd libfreenect
mkdir -p build
cd build
cmake -L -DLIBUSB_1_INCLUDE_DIR=/home/pi/libusb/libusb/ -DLIBUSB_1_LIBRARY=/usr/local/lib/libusb-1.0.so ..
make && sudo make install

wget https://github.com/OpenKinect/libfreenect/blob/master/platform/linux/udev/51-kinect.rules
sudo mv 51-kinect.rules /etc/udev/rules.d/

