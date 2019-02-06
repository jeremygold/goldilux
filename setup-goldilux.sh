#!/usr/bin/env bash

sudo apt update
sudo apt -y upgrade

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

