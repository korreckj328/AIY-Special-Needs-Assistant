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

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()

    while True:
        button.wait_for_press()
        text = recognizer.recognize()
        if text is None:
            os.system('aplay /home/pi/AIY-Special-Needs-Assistant/beep.wav')
        else:
            if 'turn on the light' in text:
                led.set_state(aiy.voicehat.LED.ON)
            elif 'switch to the vacation schedule' in text:
                os.system('aplay /home/pi/AIY-Special-Needs-Assistant/vacation.wav')
                os.system('crontab /home/pi/AIY-Special-Needs-Assistant/vacationcron.bak')
            elif 'switch to the school schedule' in text:
                os.system('aplay /home/pi/AIY-Special-Needs-Assistant/school.wav')
                os.system('crontab /home/pi/AIY-Special-Needs-Assistant/schooldayscron.bak')
            elif 'turn off the light' in text:
                led.set_state(aiy.voicehat.LED.OFF)
            elif 'blink' in text:
                led.set_state(aiy.voicehat.LED.BLINK)
            elif 'shutdown' in text:
                os.system('aplay /home/pi/AIY-Special-Needs-Assistant/shutdown.wav')
                os.system('sudo shutdown -h now')
            elif 'turn off' in text:
                os.system('aplay /home/pi/AIY-Special-Needs-Assistant/shutdown.wav')
                os.system('sudo shutdown -h now')
            elif 'reboot' in text:
                os.system('aplay /home/pi/AIY-Special-Needs-Assistant/restarting.wav')
                os.system('sudo reboot')
            elif 'restart' in text:
                os.system('aplay /home/pi/AIY-Special-Needs-Assistant/restarting.wav')
                os.system('sudo reboot')
            elif 'goodbye' in text:
                break


if __name__ == '__main__':
    main()
