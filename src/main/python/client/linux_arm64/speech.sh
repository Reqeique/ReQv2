#!/bin/bash
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -lang|--language)
    LANGUAGE="$2"
    shift # past argument
    shift # past value
    ;;
    -t|--text)
    TEXT="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    echo "Unknown option: $1"
    exit 1
    ;;
esac
done

say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_t>say "${TEXT}"


