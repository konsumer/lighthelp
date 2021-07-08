#! /bin/bash

RFSNIFFERCMD="/home/pi/433Utils/RPi_utils/RFSniffer"
DEBOUNCE=10
# Debnounce = seconds
dt=$(date '+%r %d/%m/%Y')
OLDTIME=$((`date +%s`-$DEBOUNCE))
TOGGLEFILE=/dev/shm/toggle.file

$RFSNIFFERCMD | while read line
do
    if [ "$line." == "Received 835186." ] || [ "$line."  == "Received 818562." ] || [ "$line."  == "Received 3764961." ]
    then
        NOW=`date +%s`
        if [ $(($NOW - $OLDTIME)) -lt $DEBOUNCE ]
        then
            echo "Ignoring Button Press Duplication"
            #echo "Ignoring change at $NOW / $OLDTIME"
        elif [ -e $TOGGLEFILE ]
        then
            OLDTIME=$NOW
            rm $TOGGLEFILE
            echo "Turn On"
            /home/pi/cloudtuya/l-on.py
            echo "Light Switch On at $dt"
        else
            OLDTIME=$NOW
            touch $TOGGLEFILE
            echo "Turn Off"
            /home/pi/cloudtuya/l-off.py
            echo "Light Switch Off at $dt"
        fi
    fi
done
