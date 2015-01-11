#!/bin/bash

PID=$(pidof stage/bin/python2.7)
cat /proc/$PID/maps > maps.out
