#!/bin/bash

sudo vim /etc/nginx/sites-available/bot-listener
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/bot-listener /etc/nginx/sites-enabled/
sudo nginx -t
sudo service nginx restart

sudo su -c 'echo "" > access.log'
sudo su -c 'echo "" > error.log'
sudo su -c 'echo "" > access_v4.log'
sudo su -c 'echo "" > access_v6.log'

