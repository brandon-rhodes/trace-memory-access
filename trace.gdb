file python2.7
break chdir
# display/i $pc
run test.py

# Should encounter breakpoint here.

# set debug record 2
set record full insn-number-max unlimited
record full
c

# Should encounter breakpoint here.

record goto begin
record instruction-history


#record save gdb_record.out
quit
