#!/bin/bash

gdb pwd <<EOF &>registers.out
break getcwd
run
p 100
info register
quit
EOF
