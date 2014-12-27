file python2.7
break socket
display/i $pc
run test.py
p 100
# set debug record 2
set record full insn-number-max unlimited
record full
si 1299
record save gdb_record.out
