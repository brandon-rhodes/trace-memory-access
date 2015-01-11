import subprocess

def read_addresses(trace_file):
    addresses = []
    for line in trace_file:
        fields = line.split()
        event = fields[1]
        addrstr = fields[4] if event == 'Read' else fields[2]
        address = int(addrstr.split('x')[1], 16)
        addresses.append(address)
    return addresses

def read_maps(maps_file):
    regions = []
    for line in maps_file:
        fields = line.split()
        start, end = fields[0].split('-')
        start = int(start, 16)
        end = int(end, 16)
        name = fields[5] if len(fields) > 5 else '?'
        regions.append((start, end, name))
    return regions

#nm -D -S --defined-only stage/bin/python2.7
#readelf -s stage/bin/python2.7  ->  # / addr / size

def read_symbols(binary_path):
    output = subprocess.check_output(['objdump', '-x', binary_path])
    for line in output.splitlines():
        words = line.split()
        if len(words) > 2 and words[1] == '.text':
            vma = int(words[3], 16)
            break
    output = subprocess.check_output([
        'nm', '-D', '-S', '--defined-only', binary_path])
    symbols = []
    for line in output.splitlines():
        fields = line.split()
        if len(fields) < 4:
            continue
        offset, size, flag, name = fields
        offset = int(offset, 16) - vma
        size = int(size, 16)
        symbols.append([offset, offset + size, name])
    return symbols

def classify(addresses, regions, symbols):
    for address in addresses:
        for start, end, name in regions:
            if start <= address < end:
                break
        else:
            print hex(address), 'ADDRESS NOT IN ANY MEMORY MAP'
            continue
        print hex(address), name,
        if name.endswith('/python2.7'):
            offset = address - start
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
