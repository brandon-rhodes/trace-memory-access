#!/bin/bash

set -e

PYTHON=/usr/bin/python3.4
SDE=~/sde-external-7.15.0-2015-01-11-lin/sde

LIB=stage/lib/$(basename $PYTHON)

if [ ! -f stage/python ] ;then
    mkdir -p $LIB/lib-dynload
    cp $PYTHON stage/python
    touch $LIB/os.py
fi

cp target.py $LIB/encodings.py

unset PYTHONDONTWRITEBYTECODE
$PYTHON -m py_compile stage/lib/python3.4/encodings.py

if [ $(cat /proc/sys/kernel/yama/ptrace_scope) = 1 ]
then
    echo
    echo "ERROR - as root, run: echo 0 > /proc/sys/kernel/yama/ptrace_scope"
    echo
    exit 1
fi

exec $SDE -odebugtrace /dev/stdout -- stage/python |
awk '/0x1234567/,/0x1234568/' > trace.out
