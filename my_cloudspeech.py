#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import os
import socket
import time
import threading

class assistantSettings(object):
    def __init__(self):
        settingsArray = []
        try:
            with open('/home/pi/.SpecialNeeds.config','r') as f:
                for line in f:
                    settingsArray.append(line)
        except:
            with open('/home/pi/.SpecialNeeds.config','w') as f:
                f.write('20\n')
                f.write('vacation')
            settingsArray.append('20')
            settingsArray.append('vacation')
        self.volume = int(settingsArray[0])
        self.schedule = settingsArray[1]
    
    def setVolume(self, volume):
        self.volume = volume
    
    def getVolume(self):
        return self.volume
    
    def setSchedule(self, schedule):
        self.schedule = schedule
    
    def getSchedule(self):
        return self.schedule
    
    def save(self):
        volumeString = str(self.volume) + '\n'
        with open('/home/pi/.SpecialNeeds.config','w') as f:
            f.write(volumeString)
            f.write(self.schedule)
    
class myThread(threading.Thread):
    def __init__(self,threadID,name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    
    def run(self):
        internet()

def rtime(settings):
    currentVolume = settings.getVolume()
    schedule = settings.getSchedule()
    recognizer = aiy.cloudspeech.get_recognizer()
    button = aiy.voicehat.get_button()
    aiy.audio.say('What time would you like the reminder',volume=currentVolume)
    while True:
        button.wait_for_press()
        time = recognizer.recognize(immediate=True)
        if time is not None:
            break
    if len(time) == 1:
        time = time+':00'
    elif len(time) == 2:
        time = time+':00'
    elif len(time) == 3:
        time = time[0]+':'+time[1]+time[2]
    time = time.split(':')
    aiy.audio.say('A M or P M?',volume=10)
    while True:
        button.wait_for_press()
        ampm = recognizer.recognize(immediate=True)
        if ampm == 'a.m.' or ampm == 'p.m.':
            break
    if ampm == 'p.m.':
        time[0] = str(int(time[0]) + 12)
    aiy.audio.say('Repeat on what days?  You can say every day, week days',volume=currentVolume)
    aiy.audio.say('weekends, or a specific day.',volume=currentVolume)
    while True:
        button.wait_for_press()
        days = recognizer.recognize(immediate=True)
        if days == 'everyday':
            days = '*'
            break
        elif days == 'weekdays':
            days = 'MON,TUE,WED,THU,FRI'
            break
        elif days == 'weekends':
            days = 'SAT,SUN'
            break
        elif days == 'Mondays':
            days = 'MON'
            break
        elif days == 'Tuesdays':
            days = 'TUE'
            break
        elif days == 'Wednesdays':
            days = 'WED'
            break
        elif days == 'Thursdays':
            days = 'THU'
            break
        elif days == 'Fridays':
            days = 'FRI'
            break
        elif days == 'Saturdays':
            days = 'SAT'
            break
        elif days == 'Sundays':
            days = 'SUN'
            break
        else:
            aiy.audio.say('Repeat on what days?  You can say every day, week days',volume=currentVolume)
            aiy.audio.say('weekends, or a specific day.',volume=currentVolume)
    crontime = '{:s} {:s} * * {:s}'.format(time[1],time[0],days)
    return crontime

def rmessage(settings):
    currentVolume = settings.getVolume()
    schedule = settings.getSchedule()
    recognizer = aiy.cloudspeech.get_recognizer()
    while True:
        button = aiy.voicehat.get_button()
        aiy.audio.say('What would you like the reminder to say?',volume=currentVolume)
        button.wait_for_press()
        message = recognizer.recognize(immediate=True)
        if message is not None:
            return message

def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    led = aiy.voicehat.get_led()
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        led.set_state(aiy.voicehat.LED.ON)
    except:
        led.set_state(aiy.voicehat.LED.BLINK)

def volumeUP(settings):
    currentVolume = settings.getVolume()
    schedule = settings.getSchedule()
    volume = currentVolume + 2
    settings.setVolume(volume)
    settings.save()
    aiy.audio.say('ok',volume=volume)

def volumeDOWN(settings):
    currentVolume = settings.getVolume()
    schedule = settings.getSchedule()
    volume = currentVolume - 2
    settings.setVolume(volume)
    settings.save()
    aiy.audio.say('ok',volume=volume)

def main():
    
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('shutdown')
    recognizer.expect_phrase('restart')
    recognizer.expect_phrase('turn off')
    recognizer.expect_phrase('reboot')
    recognizer.expect_phrase('volume up')
    recognizer.expect_phrase('volume down')
    recognizer.expect_phrase('switch to the vacation schedule')
    recognizer.expect_phrase('switch to the school schedule')
    recognizer.expect_phrase('goodbye')
    recognizer.expect_phrase('add a reminder')
    recognizer.expect_phrase('help')
    recognizer.expect_phrase('clear all reminders')

    button = aiy.voicehat.get_button()
    aiy.audio.get_recorder().start()
    
    testarray = []
    try:
        with open('/home/pi/schedule.cronbak','r') as f:
            for line in f:
                testarray.append(line)
        print(testarray)
    except:
        with open('/home/pi/schedule.cronbak','w') as f:
            f.write('XDG_RUNTIME_DIR=/run/user/1000\n')
    
    while True:
        internetThread = myThread(1,'internetcheck')
        internetThread.start()
        settings = assistantSettings()
        currentVolume = settings.getVolume()
        schedule = settings.getSchedule()
        button.wait_for_press()
        text = recognizer.recognize()
        if text is None:
            aiy.audio.say('I am sorry, I did not catch that, for help say help.',volume=currentVolume)
        else:
            if 'add a reminder' in text:
                time = rtime(settings)
                message = rmessage(settings)
                cronline = '{:s} /home/pi/AIY-projects-python/src/examples/voice/reminder_playback.py "{:s}"\n'.format(time,message)
                with open('/home/pi/schedule.cronbak','a') as f:
                    f.write(cronline)
                os.system('crontab /home/pi/schedule.cronbak')
                aiy.audio.say('Your reminder is now set',volume=currentVolume)
            elif 'switch to the vacation schedule' in text:
                aiy.audio.say('This function is not yet implemented.',volume=currentVolume)
            elif 'switch to the school schedule' in text:
                aiy.audio.say('This function is not yet implemented.',volume=currentVolume)
            elif 'volume up' in text:
                volumeUP(settings)
            elif 'volume down' in text:
                volumeDOWN(settings)
            elif 'shutdown' in text:
                aiy.audio.say("Shutting down",volume=currentVolume)
                os.system('sudo shutdown -h now')
            elif 'turn off' in text:
                aiy.audio.say("Shutting down",volume=currentVolume)
                os.system('sudo shutdown -h now')
            elif 'reboot' in text:
                aiy.audio.say("Restarting",volume=currentVolume)
                os.system('sudo reboot')
            elif 'restart' in text:
                aiy.audio.say("Restarting",volume=currentVolume)
                os.system('sudo reboot')
            elif 'clear all reminders' in text:
                os.system('crontab -r')
                with open('/home/pi/schedule.cronbak','w') as f:
                    f.write('XDG_RUNTIME_DIR=/run/user/1000\n')
                aiy.audio.say("All reminders deleted")
            elif 'help' in text:
                aiy.audio.say("To adjust the volume, say volume up or down", volume=currentVolume)
                aiy.audio.say("To add a reminder say, add a reminder.", volume=currentVolume)
                aiy.audio.say("To delete all reminders say, clear all reminders.", volume=currentVolume)
                aiy.audio.say("To shut down the system, say shut down or turn off", volume=currentVolume)
                aiy.audio.say("To restart the system, say reboot or restart", volume=currentVolume)


if __name__ == '__main__':
    main()
