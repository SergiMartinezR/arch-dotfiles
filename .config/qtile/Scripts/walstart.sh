#!/bin/sh

#Starts pywal
wal -i $HOME/Documents/Wallpapers --iterative

#Reloads qtile
xdotool key super+Control_L+r

#Reloads dunst
/bin/bash /home/sergi/.config/dunst/reload.sh

#Reloads discord theme
pywal-discord


