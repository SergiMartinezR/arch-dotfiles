#!/bin/sh
 
printf "%s" "$(/usr/sbin/ifconfig enp3s0 | grep "inet " | awk '{print $2}')"
