import struct

MAGIC = struct.pack('!I', 0x20091016)

def int_bytes(n):
    return struct.pack('I', n)

def dump(data, offset):
    step = struct.calcsize('I')
    print 'Step size:', step, '-' * 40
    for i in range(offset - 15 * step, offset + 25 * step, step):
        excerpt = data[i:i+step]
        n, = struct.unpack('I', excerpt)
        if i == offset:
            print '===>',
        print hex(i), hex(n)

record_types = ['END', 'REG', 'MEM']

def main():
    with open('gdb_record.out', 'rb') as f:
        data = f.read()

    assert data.count(MAGIC) == 1
    i = data.index(MAGIC) + len(MAGIC)

    while True:

        record_type = record_types[ord(data[i])]
        i += 1
        if record_type == 'END':
            signal, count = struct.unpack('!II', data[i:i+8])
            i += 8
            if count == 0:
                break
            print record_type, signal, count
            print
        elif record_type == 'REG':
            register, value = struct.unpack('!II', data[i:i+8])
            i += 8
            print record_type, register, value
        elif record_type == 'MEM':
            length, address = struct.unpack('!IQ', data[i:i+12])
            i += 12
            value = data[i:i+length]
            i += length
            print record_type, length, hex(address), repr(value)
        else:
            print 'Unknown record type', record_type
            return

    return

    if True:
        lower = n - 10
        upper = n + 10

        for i in range(0, len(data), 4):
            excerpt = data[i:i+4]
            value, = struct.unpack('I', excerpt)
            if lower <= value <= upper:
                print hex(i), value

        print '-' * 20

    dump(data, 0xd2d4f4)
    dump(data, 0xd30ee0)

    print struct.calcsize('L')

if __name__ == '__main__':
    main()
