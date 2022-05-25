#!/usr/bin/env python3

import subprocess
import shlex

# Returns whether the keyboard input was fired.
def parse_twofingers_action(line):
    device, event, time, details = line.strip().split(maxsplit=3)
    if event == 'POINTER_SCROLL_FINGER':
        vert, v_value, horiz, h_value, unused = details.split(maxsplit=4)
        # action was not vertical scrolling
        if vert.strip() == 'vert' and v_value.strip() == '0.00/0.0':
            l, r = h_value.split('/')
            if (float(l) > 5): # The action was like forward
                subprocess.Popen(shlex.split('xdotool key alt+Left'))
                return True
            if (float(l) < -5): # The action like backward
                subprocess.Popen(shlex.split('xdotool key alt+Right'))
                return True
    return False

def main():
    command = 'stdbuf -oL -- libinput debug-events'
    cmd = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
    ignore = 0
    for line in cmd.stdout:
        # skip 10 lines if an action was fired.
        if 0 < ignore:
            ignore = ignore - 1
            continue
        fired = parse_twofingers_action(line)
        if fired:
            ignore = 10

if __name__ == '__main__':
    main()
