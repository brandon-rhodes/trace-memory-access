#!/bin/bash

#gdb -batch -x trace.gdb

if [ ! -f stage/bin/python2.7 ] ;then
    mkdir -p stage/bin
    mkdir -p stage/lib/python2.7
    cp /usr/bin/python2.7 stage/bin/python2.7
    touch stage/lib/python2.7/os.py
fi

cp site.py stage/lib/python2.7/site.py

exec stage/bin/python2.7
