# twofingers-gesture
twofingers-gesture enables gestures with 2 fingers on Linux (X11, gnome).

## Background and Idea
libinput doesn't support 2 fingers gestures so users can't go forward/backward browser histroy, etc ... with 2 fingers swipe.
However, other major OSs, Windows and Mac are supporting this feature, even ChromeOS does.

Even libinput doesn't support 2 fingers swipe, `libinput debug-events` exposes 2 fingers actions with details like this:
```
 event6   POINTER_SCROLL_FINGER   +2.867s       vert 0.00/0.0 horiz -7.03/0.0* (finger)
 event6   POINTER_SCROLL_FINGER   +2.873s       vert 0.00/0.0 horiz -7.47/0.0* (finger)
 event6   POINTER_SCROLL_FINGER   +2.880s       vert 0.00/0.0 horiz -7.03/0.0* (finger)
 event6   POINTER_SCROLL_FINGER   +2.887s       vert 0.00/0.0 horiz -7.47/0.0* (finger)
 event6   POINTER_SCROLL_FINGER   +2.894s       vert 0.00/0.0 horiz -7.03/0.0* (finger)
 event6   POINTER_SCROLL_FINGER   +2.901s       vert 0.00/0.0 horiz -5.27/0.0* (finger)
```

twofingers-gesture parses the lines and checks vert / horiz values and if the action was like forward/backward swipe then maps to `xdotool key ...` and executes it.

This logic eventualy converts swipe actions to keyboard inputs.


## Registering this to autostart
Write this file to `${XDG_CONFIG_HOME}/autostart/${name}.desktop` usually ~/.config/.

```
[Desktop Entry]
Type=Application
NoDisplay=true
Terminal=false
Name=twofingers-gesture
Icon=
Exec=/PATH_TO/main.py
Comment=
Categories=System;
```

## Troubleshooting
`main.py` contains only ~40 lines with comments, you can easily understand that.
1. Run xdotool and verify it works.
2. Run libinput debug-events and verify it works.
3. Make sure that you are in `input` group.

The values in `main.py` are customized for my environment (debian rodete on X1 carbon), you can watch `libinput debug-events` logs and update `main.py`.

## TODO
Config, rewrite with golang
