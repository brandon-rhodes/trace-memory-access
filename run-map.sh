#!/bin/bash

PID=$(pidof -s stage/python) && cat /proc/$PID/maps > maps.out.new &&
mv maps.out.new maps.out
