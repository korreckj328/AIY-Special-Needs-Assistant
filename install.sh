#!/bin/bash
cp my_cloudspeech.py /home/pi/AIY-projects-python/src/examples/voice
cp reminder_playback.py /home/pi/AIY-projects-python/src/examples/voice
su pi -c 'cp .SpecialNeeds.config /home/pi/.SpecialNeeds.config'
cd /home/pi/AIY-projects-python/src/examples/voice
chmod +x my_cloudspeech.py
chmod +x reminder_playback.py
cd /home/pi/AIY-Special-Needs-Assistant
sudo cp SpecialNeeds.service /lib/systemd/system/
sudo systemctl enable SpecialNeeds.service
sudo service SpecialNeeds start

