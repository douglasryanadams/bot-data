#!/bin/bash

sudo vim /etc/nginx/sites-available/bot-listener
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/bot-listener /etc/nginx/sites-enabled/
sudo vim /var/www/html/base.html
sudo nginx -t
sudo service nginx restart

sudo su -c 'echo "" > /var/log/nginx/access.log'
sudo su -c 'echo "" > /var/log/nginx/error.log'
sudo su -c 'echo "" > /var/log/nginx/access_v4.log'
sudo su -c 'echo "" > /var/log/nginx/access_v6.log'

