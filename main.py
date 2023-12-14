#!/usr/bin/env python3

import subprocess
import shlex

pinch_in_progress = False
last_scale_factor = 1.0

# Returns whether the keyboard input was fired.
def parse_twofingers_action(line):
    device, event, time, details = line.strip().split(maxsplit=3)
    if event == 'POINTER_SCROLL_FINGER':
        vert, v_value, horiz, h_value, unused = details.split(maxsplit=4)
        # action was not vertical scrolling
        if vert.strip() == 'vert' and v_value.strip() == '0.00/0.0':
            l, r = h_value.split('/')
            if (float(l) > 5):  # The action was like forward
                subprocess.Popen(shlex.split('xdotool key alt+Left'))
                return True
            if (float(l) < -5):  # The action like backward
                subprocess.Popen(shlex.split('xdotool key alt+Right'))
                return True
    return False

def parse_pinch_gesture(line):
    global pinch_in_progress, last_scale_factor

    if 'GESTURE_PINCH_BEGIN' in line:
        pinch_in_progress = True
        last_scale_factor = 1.0
        return False

    elif 'GESTURE_PINCH_UPDATE' in line and pinch_in_progress:
        try:
            # Split the line and extract the scale factor
            parts = line.split()
            scale_factor_str = parts[-3]  # The scale factor is now the third last element
            scale_factor = float(scale_factor_str)

            # Implement the logic for pinch gestures
            if scale_factor < 0.8:  # Threshold for pinch-in (zoom out)
                subprocess.Popen(shlex.split('xdotool key Ctrl+minus'))
                pinch_in_progress = False
                return True
            elif scale_factor > 1.2:  # Threshold for pinch-out (zoom in)
                subprocess.Popen(shlex.split('xdotool key Ctrl+plus'))
                pinch_in_progress = False
                return True

        except ValueError as e:
            print("Error parsing line:", line)
            print("Exception:", e)
            return False

    elif 'GESTURE_PINCH_END' in line:
        pinch_in_progress = False
        return False

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
        if parse_twofingers_action(line) or parse_pinch_gesture(line):
            ignore = 10

if __name__ == '__main__':
    main()
