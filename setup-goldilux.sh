#!/usr/bin/env bash

sudo apt update
sudo apt -y upgrade

if [ ! -f ~/processing-3.5.3/bin/processing ]; then
  echo "Installing Processing"
  wget -O processing.tgz http://download.processing.org/processing-3.5.3-linux-armv6hf.tgz
  tar xvzf processing.tgz
fi

