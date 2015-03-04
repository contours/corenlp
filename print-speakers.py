#! /usr/bin/env python3

# Given a transcript like this...
#
# WILLOUGHBY ANDERSON:
# This is an interview with Arthur J. Hanes, Jr.
# If you could please just state your name we'll see how the mike is doing.
# ARTHUR HANES, JR.:
# My name is Arthur J. Hanes, Jr.
# People call me Art.
# Some people, I guess, by virtue of the honorific call me Judge.
#
# ...print the speaker for each line:

# WILLOUGHBY ANDERSON
# WILLOUGHBY ANDERSON
# ARTHUR HANES, JR.
# ARTHUR HANES, JR.
# ARTHUR HANES, JR.

import sys

if len(sys.argv) < 2:
    print('Usage: print-speakers [transcript]', file=sys.stderr)
    sys.exit(1)

speakers = []
labels = []
while True:
    name = input('Speaker %s [blank if no more speakers]:')
    if not name: break
    speakers.append(name + '\n')
    labels.append(name + ':\n')

if len(speakers) < 2:
    print('Need at least two speakers.', file=sys.stderr)
    sys.exit(1)
    
f = open(sys.argv[1])
lines = f.readlines()
speaker = None
for l in lines:
    if l in speakers:
        print(l, end='')
        continue
    try:
        speaker = speakers[labels.index(l)]
        continue
    except:
        print(speaker, end='')
