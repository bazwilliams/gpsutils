#!/bin/sh

xrandr --output LVDS --mode 1024x600 --fb 800x480 --scale 0.8x0.8
#xrandr --fb 1024x768 --output LVDS --pos 0x0 --panning 1024x724+0+0
/home/barry/cxoffice/bin/wine --bottle iGo --workdir /home/barry/.cxoffice/iGo/drive_c/Program\ Files/iGO8/ -- /home/barry/.cxoffice/iGo/drive_c/Program\ Files/iGO8/iGo_pc.exe
xrandr --output LVDS --mode 1024x600 --fb 1024x600 --scale 1x1
