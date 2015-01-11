

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

def classify(addresses, regions):
    for address in addresses:
        for start, end, name in regions:
            if start <= address < end:
                print hex(address), name
                break
        else:
            print hex(address), 'ADDRESS NOT IN ANY MEMORY MAP'

if __name__ == '__main__':
    addresses = read_addresses(open('trace.out'))
    regions = read_maps(open('maps.out'))
    classify(addresses, regions)
