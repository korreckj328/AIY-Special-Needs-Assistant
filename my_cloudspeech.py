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

def rtime():
    recognizer = aiy.cloudspeech.get_recognizer()
    button = aiy.voicehat.get_button()
    aiy.audio.say('What time would you like the reminder',volume=10)
    button.wait_for_press()
    time = recognizer.recognize(immediate=True)
    if len(time) == 1:
        time = time+':00'
    elif len(time) == 2:
        time = time+':00'
    elif len(time) == 3:
        time = time[0]+':'+time[1]+time[2]
    time = time.split(':')
    aiy.audio.say('A M or P M?',volume=10)
    button.wait_for_press()
    ampm = recognizer.recognize(immediate=True)
    if ampm == 'p.m.':
        time[0] = str(int(time[0]) + 12)
    aiy.audio.say('Repeat on what days?  You can say every day, week days, weekends, or a specific day.',volume=10)
    button.wait_for_press()
    days = recognizer.recognize(immediate=True)
    if days == 'everyday':
        days = '*'
    elif days == 'weekdays':
        days = 'MON,TUE,WED,THU,FRI'
    elif days == 'weekends':
        days = 'SAT,SUN'
    elif days == 'Monday':
        days = 'MON'
    elif days == 'Tuesday':
        days = 'TUE'
    elif days == 'Wednesday':
        days = 'WED'
    elif days == 'Thursday':
        days = 'THU'
    elif days == 'Friday':
        days = 'FRI'
    elif days == 'Saturday':
        days = 'SAT'
    elif days == 'Sunday':
        days = 'SUN'
    crontime = '{:s} {:s} * * {:s} '.format(time[1],time[0],days)
    return crontime

def rmessage():
    recognizer = aiy.cloudspeech.get_recognizer()
    button = aiy.voicehat.get_button()
    aiy.audio.say('What would you like the reminder to say?',volume=10)
    button.wait_for_press()
    message = recognizer.recognize(immediate=True)
    return message

def main():
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('turn off the light')
    recognizer.expect_phrase('turn on the light')
    recognizer.expect_phrase('blink')
    recognizer.expect_phrase('shutdown')
    recognizer.expect_phrase('restart')
    recognizer.expect_phrase('turn off')
    recognizer.expect_phrase('reboot')
    recognizer.expect_phrase('switch to the vacation schedule')
    recognizer.expect_phrase('switch to the school schedule')
    recognizer.expect_phrase('goodbye')
    recognizer.expect_phrase('add a reminder')

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()

    while True:
        button.wait_for_press()
        text = recognizer.recognize()
        if text is None:
            aiy.audio.say('I am sorry, I did not catch that.',volume=10)
        else:
            if 'add a reminder' in text:
                time = rtime()
                message = rmessage()
                cronline = '{:s} /home/pi/AIY-projects-python/src/examples/voice/reminder_playback.py "{:s}"\n'.format(time,message)
                with open('/home/pi/schedule.cronbak','a') as f:
                    f.write(cronline)
                os.system('crontab /home/pi/schedule.cronbak')
            if 'turn on the light' in text:
                led.set_state(aiy.voicehat.LED.ON)
            elif 'switch to the vacation schedule' in text:
                aiy.audio.say('This function is not yet implemented.',volume=10)
            elif 'switch to the school schedule' in text:
                aiy.audio.say('This function is not yet implemented.',volume=10)
            elif 'turn off the light' in text:
                led.set_state(aiy.voicehat.LED.OFF)
            elif 'blink' in text:
                led.set_state(aiy.voicehat.LED.BLINK)
            elif 'shutdown' in text:
                aiy.audio.say("Shutting down",volume=10)
                os.system('sudo shutdown -h now')
            elif 'turn off' in text:
                aiy.audio.say("Shutting down",volume=10)
                os.system('sudo shutdown -h now')
            elif 'reboot' in text:
                aiy.audio.say("Restarting",volume=10)
                os.system('sudo reboot')
            elif 'restart' in text:
                aiy.audio.say("Restarting",volume=10)
                os.system('sudo reboot')
            elif 'goodbye' in text:
                break


if __name__ == '__main__':
    main()
