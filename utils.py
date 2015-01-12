import subprocess

def addr_of(s):
    """Where `s` could be '*(UINT32*)0xbfafa080' or '0x2' or '0'."""
    if '0x' in s:
        s = s.split('0x')[1]
    return int(s, 16)

def read_events(trace_file):
    for line in trace_file:
        fields = line.split()
        event = fields[1]
        f2 = addr_of(fields[2])
        if event == 'INS':
            address = f2
            value = None
        else:
            f4 = addr_of(fields[4])
            if event == 'Read':
                address = f4
                value = f2
            else:
                address = f2
                value = f4
        yield (event, address, value)

def read_maps(maps_file):
    regions = []
    for line in maps_file:
        fields = line.split()
        start, end = fields[0].split('-')
        start = int(start, 16)
        end = int(end, 16)
        permissions = fields[1]
        name = fields[5] if len(fields) > 5 else '?'
        regions.append((start, end, permissions, name))
    return regions

def read_symbols(binary_path):
    cmd = ['readelf', '-l', binary_path]
    output = subprocess.check_output(cmd)
    for line in output.splitlines():
        line = line.strip()
        if line.startswith('LOAD') and ('RW' not in line):
            words = line.split()
            vma = int(words[3].lstrip('0x'), 16)
            break

    cmd = ['readelf', '-s', binary_path]
    output = subprocess.check_output(cmd)
    symbols = []
    lines = iter(output.splitlines())
    line = next(lines)
    while 'Num:' not in line:
        line = next(lines)
    for line in lines:
        fields = line.split()
        if fields[6] == 'UND':
            continue

        #    300: 083ae3c0   196 OBJECT  GLOBAL DEFAULT   24 PyTraceBack_Type

        offset = int(fields[1], 16) - vma
        size = int(fields[2])
        name = fields[7]
        # if name == 'PyEval_EvalFrameEx':
        #     print 'PyEval_EvalFrameEx', offset
        symbols.append([offset, offset + size, name])

    return symbols

def classify(events, regions, symbols):
    for event, address, value in events:
        for start, end, permissions, name in regions:
            if start <= address < end:
                break
        else:
            print hex(address), 'ADDRESS NOT IN ANY MEMORY MAP'
            continue
        if value is None:
            value = '-'
        else:
            value = '0x%x=%d' % (value, value)
        print event.ljust(4), hex(address).rstrip('L'),
        print value, permissions, name,
        could_be_text_segment = (permissions[1] == '-')
        if name.endswith('/python') and could_be_text_segment:
            offset = address - start
            print offset,
            for start, end, name in symbols:
                if start <= offset < end:
                    print name,
                    break
            else:
                print '<unnamed_text>',
        print

if __name__ == '__main__':
    events = list(read_events(open('trace.out')))
    regions = read_maps(open('maps.out'))
    symbols = read_symbols('stage/python')
    classify(events, regions, symbols)
