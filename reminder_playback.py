#!/usr/bin/env python3
import sys
import aiy.audio
import aiy.cloudspeech
import aiy.voicehat

name = sys.argv[1]
aiy.audio.say(name,volume=10)

