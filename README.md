# Goldilux

Project files for an exhibition at Queenstown LUMA / Wellington LUX festivals.

# Initial Raspberry PI setup
* Download and install Raspbian Stretch Desktop from https://www.raspberrypi.org/downloads/raspbian/

      $ sudo raspi-config

* Set the hostname to goldilux2 (or whatever is the next number)
* Expand the filesystem
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

* Clone goldilux repo
    $ git clone git@github.com:jeremygold/goldilux.git

* TODO: Install processing

      $ cd goldilux
      $ ./setup-goldilux.sh
