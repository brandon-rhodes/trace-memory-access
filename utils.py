import subprocess

def read_addresses(trace_file):
    addresses = []
    for line in trace_file:
        fields = line.split()
        event = fields[1]
        addrstr = fields[4] if event == 'Read' else fields[2]
        address = int(addrstr.split('0x')[1], 16)
        addresses.append(address)
    return addresses

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
        if name == 'PyEval_EvalFrameEx':
            print 'PyEval_EvalFrameEx', offset
        symbols.append([offset, offset + size, name])

    return symbols

def classify(addresses, regions, symbols):
    for address in addresses:
        for start, end, permissions, name in regions:
            if start <= address < end:
                break
        else:
            print hex(address), 'ADDRESS NOT IN ANY MEMORY MAP'
            continue
        print hex(address), permissions, name,
        could_be_text_segment = (permissions[1] == '-')
        if name.endswith('/python2.7') and could_be_text_segment:
            offset = address - start
            print offset,
            for start, end, name in symbols:
                if start <= offset < end:
                    print name,
                    break
            else:
                print 'UNKNOWN',
        print

if __name__ == '__main__':
    addresses = read_addresses(open('trace.out'))
    regions = read_maps(open('maps.out'))
    symbols = read_symbols('stage/bin/python2.7')
    classify(addresses, regions, symbols)
