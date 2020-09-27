#!/bin/bash

if [ -z "$LOGIN_USER" ]; then
  echo "Please set LOGIN_USER";
fi

passwd
update-alternatives --config editor

apt update
apt upgrade
apt autoremove
apt clean

apt install sudo vim net-tools nginx

# Create User, Make Admin, Allow SSH, Disable Root SSH
adduser "$LOGIN_USER"
addgroup admin
adduser "$LOGIN_USER" admin

vim /etc/ssh/sshd_config
# PermitRootLogin no
service ssh restart

