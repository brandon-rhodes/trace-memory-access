#!/bin/bash

if [ ! -f stage/bin/python2.7 ] ;then
    mkdir -p stage/bin
    mkdir -p stage/lib/python2.7
    cp /usr/bin/python2.7 stage/bin/python2.7
    touch stage/lib/python2.7/os.py
fi

cp site.py stage/lib/python2.7/site.py

exec ~/sde-external-7.8.0-2014-10-02-lin/sde -debugtrace -- stage/bin/python2.7
