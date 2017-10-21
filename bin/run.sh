#!/bin/bash

GM_REPO=$HOME/src/pogo-game-master/archive
BIN=$(dirname $0)

GAME_MASTER=$GM_REPO/$($BIN/adb-pull.sh $GM_REPO)
if [ $? -eq 1 ]; then
    exit 1
fi

GAME_MASTER_TXT=$GAME_MASTER.txt
GAME_MASTER_JSON=$GAME_MASTER.json

$BIN/decode.sh $GAME_MASTER > $GAME_MASTER_TXT
$BIN/master2json.py $GAME_MASTER_TXT | json_pp > $GAME_MASTER_JSON

cp $GAME_MASTER $GM_REPO/../current
cp $GAME_MASTER_TXT $GM_REPO/../current.txt
cp $GAME_MASTER_JSON $GM_REPO/../current.json
