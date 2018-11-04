#!/bin/bash

# Steps for setting up Raspberry Pi 3's with a fresh installation of Raspian
# for use in IoT Security Gateway
#
# File created: 9 January 2018 by Matt McCormack
# File updated: 23 August 2018 by Matt McCormack
#
# Invocation example ./RaspberryPI_setup.sh <STEP#>

# Step 1 - Get latest software
if [ $1 == 1 ]; then
    sudo apt-get -y update
    sudo apt-get -y dist-upgrade
    sudo reboot
fi

# Step 2 - Get latest firmware
if [ $1 == 2 ]; then
    sudo rpi-update
    sudo reboot
fi

# Step 3 - Install standard packages & enable SSH
if [ $1 == 3 ]; then
    sudo apt-get -y update
    sudo apt-get -y install python python-dev python-pip emacs vim \
	 iperf3 nmap python-ipaddress python-subprocess32 \
	 apt-transport-https ca-certificates \
	 docker openvswitch-common openvswitch-switch openvswitch-dbg \
	 isc-dhcp-server wireshark tcpdump wavemon netcat hping3 \
	 iptables-persistent

    sudo dpkg-reconfigure wireshark-common
    sudo adduser $USER wireshark

    #TODO: Update getting hostapd to use modified linux_ioctl.c file
    
    curl -sSL https://get.docker.com | sh

    #TODO: Update to get my modified version of OVS
    cd /usr/bin
    sudo wget https://raw.githubusercontent.com/openvswitch/ovs/master/utilities/ovs-docker
    sudo chmod a+rwx ovs-docker
    
    sudo systemctl enable ssh
    sudo systemctl start ssh
    sudo dpkg-reconfigure openssh-server

    sudo reboot
fi

