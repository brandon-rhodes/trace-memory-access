file python2.7
break chdir
run test.py

# Should encounter breakpoint here.

display/i $pc
x/i $pc
si
si
si
si
quit

# set debug record 2
set record full insn-number-max unlimited
record full
c

# Should encounter breakpoint here.

record save gdb_record.out
quit
