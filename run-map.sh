#!/bin/bash

PID=$(pidof stage/python) && cat /proc/$PID/maps > maps.out
