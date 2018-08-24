#!/bin/bash

sudo systemctl stop SpecialNeeds
sudo systemctl disable SpecialNeeds
sudo rm /lib/systemd/system/SpecialNeeds.service
sudo systemctl daemon-reload
sudo systemctl reset-failed
rm /home/pi/schedule.cronbak
rm /home/pi/.SpecialNeeds.config
su pi -c 'crontab -r'

