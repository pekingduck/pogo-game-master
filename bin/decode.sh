#!/bin/bash

# The src/ directory where https://github.com/AeonLucid/POGOProtos
# was cloned
PROTOS_TOP=$HOME/src/POGOProtos/src

PROTOS_TEMPLATE=$PROTOS_TOP/POGOProtos/Networking/Responses/DownloadItemTemplatesResponse.proto
PROTOS_TARGET="POGOProtos.Networking.Responses.DownloadItemTemplatesResponse"

# $1 is the game master file
protoc --proto_path="$PROTOS_TOP" \
       --decode="$PROTOS_TARGET" \
       "$PROTOS_TEMPLATE" < $1
