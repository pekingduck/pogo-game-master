#!/bin/bash

# https://stackoverflow.com/questions/11074671/adb-pull-multiple-files#11250068
ADB=adb
STATE=`adb get-state 2>/dev/null`
if [ "$STATE" != "device" ]; then
    echo device not connected.
    exit 1
fi

GAME_MASTER=$($ADB shell 'ls /sdcard/Android/data/com.nianticlabs.pokemongo/files/remote_config_cache/*GAME_MASTER')

# $1 is the dest dir
$ADB pull $GAME_MASTER $1 > /dev/null 2>&1
echo $(basename $GAME_MASTER)
