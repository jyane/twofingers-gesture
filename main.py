#!/usr/bin/env python3

import subprocess
import shlex
import sys

# Default thresholds for different devices
dev_thresh = {
    "lenovo": {"in": 0.8, "out": 1.2},
    "apple": {"in": 0.9, "out": 1.1}
}

# Determine device type from command-line arguments
dev = "lenovo"  # Default device type
if len(sys.argv) > 1:
    dev = sys.argv[1]
    if dev not in dev_thresh:
        print(f"Device '{dev}' not recognized. Using default.")
        dev = "lenovo"

pinch_in_progress = False
last_scale = 1.0

def parse_twofingers(line):
    # Implement your logic for two-finger actions here
    pass

def parse_pinch(line):
    global pinch_in_progress, last_scale

    if 'GESTURE_PINCH_BEGIN' in line:
        pinch_in_progress = True
        last_scale = 1.0
        return False

    elif 'GESTURE_PINCH_UPDATE' in line and pinch_in_progress:
        try:
            scale = float(line.split()[-3])
            if scale < dev_thresh[dev]["in"]:
                subprocess.Popen(shlex.split('xdotool key Ctrl+minus'))
                pinch_in_progress = False
                return True
            elif scale > dev_thresh[dev]["out"]:
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

def parse_swipe(line, dev):
    if 'POINTER_SCROLL_FINGER' in line:
        try:
            parts = line.split()
            horiz_index = parts.index('horiz')
            horiz_scroll = float(parts[horiz_index + 1].split('/')[0])

            swipe_thresh = 5.0
            if dev == "apple":
                # Reverse gestures for Apple Magic Trackpad
                left_action = 'xdotool key alt+Right'
                right_action = 'xdotool key alt+Left'
            else:
                left_action = 'xdotool key alt+Left'
                right_action = 'xdotool key alt+Right'

            if horiz_scroll > swipe_thresh:
                subprocess.Popen(shlex.split(left_action))
                return True
            elif horiz_scroll < -swipe_thresh:
                subprocess.Popen(shlex.split(right_action))
                return True
        except (ValueError, IndexError) as e:
            print("Error parsing line:", line)
            print("Exception:", e)

    return False

def main():
    command = 'stdbuf -oL -- libinput debug-events'
    cmd = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

    for line in cmd.stdout:
        if parse_twofingers(line) or parse_pinch(line) or parse_swipe(line, dev):
            pass

if __name__ == '__main__':
    main()
