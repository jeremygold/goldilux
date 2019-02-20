# Goldilux

Project files for an exhibition at Queenstown LUMA / Wellington LUX festivals.

# Initial Raspberry PI setup
* Download and install Raspbian Stretch Desktop from https://www.raspberrypi.org/downloads/raspbian/

      $ sudo raspi-config

* Set the hostname to goldiluxX (where X is the next number)
* Expand the filesystem (Might be done automatically on first boot)
* Enable ssh

* Copy goldilux keys to rpi (From another machine, assuming they're in ~/.ssh)

      $ scp goldilux_rsa* pi@goldilux2:/home/pi/.ssh/

* On the rpi, disable password login for pi user

      $ sudo vi /etc/ssh/sshd_config

* Set the following entries:

      ChallengeResponseAuthentication no
      PasswordAuthentication no
      UsePAM no

* Then restart the sshd service:

      $ sudo systemctl restart ssh.service

* Set up ssh config for github:

      $ vi ~/.ssh/config

      Host github.com
        HostName github.com
        IdentityFile ~/.ssh/goldilux_rsa
        User git

* Clone goldilux repo and run installation script

      $ git clone git@github.com:jeremygold/goldilux.git
      $ cd goldilux
      $ ./setup-goldilux.sh

* Run processing (on the PI for gui)

      $ processing-3.5.3/processing &

* Install Kinect support: Sketch -> Import Library... -> Add Library, and filter on Kinect
* Install "Open Kinect for Processing"