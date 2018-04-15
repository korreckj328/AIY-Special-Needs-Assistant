#!/bin/bash
cp my_cloudspeech.py /home/pi/AIY-projects-python/src/examples/voice
cd /home/pi/AIY-projects-python/src/examples/voice
chmod +x my_cloudspeech.py
cd /home/pi/AIY-Special-Needs-Assistant
sudo cp SpecialNeeds.service /lib/systemd/system/
sudo systemctl enable SpecialNeeds.service
sudo service SpecialNeeds start

