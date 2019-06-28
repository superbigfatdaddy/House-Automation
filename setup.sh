#!/usr/bin/env bash -e
#Create config.ini file
if [ ! -e config.ini ]
then
    cp config.ini.default config.ini
fi


PYTHON=`which python3`
VENV=venv

if [ -f "$PYTHON" ]
then
    if [ ! -d $VENV ]
    then
        $PYTHON -m venv $VENV
    else
        if [ -e $VENV/bin/python2 ]
        then
        rm -r $VENV
        $PYTHON -m venv $VENV
        fi
    fi
    . $VENV/bin/activate
    pip3 install -r requirements.txt
else
    >&2 echo "Cannot find Python 3. Please install it."
fi
