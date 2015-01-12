#!/bin/bash

grep '        TARGET' ~/Python-3.4.0/Python/ceval.c |
sed 's/.*(//;s/).*//' |
nl
