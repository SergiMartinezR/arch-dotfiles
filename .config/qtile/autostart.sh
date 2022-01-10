#!/bin/sh

#Run a shell script that starts wal and all its config
/bin/bash /home/sergi/.config/qtile/Scripts/walstart.sh &
#Sets the wallpaper (or desktop background)
#feh --bg-fill /home/sergi/Documents/Wallpapers/shapes-3-1920×1080.jpg &
# compositor
picom --experimental-backends &
#opens sxhkd
sxhkd &