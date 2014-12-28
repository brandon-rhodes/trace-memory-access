import struct

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

def main():
    with open('gdb_record.out', 'rb') as f:
        data = f.read()

    n = 886357

    if False:
        lower = n - 10
        upper = n + 10

        for i in range(0, len(data), 4):
            excerpt = data[i:i+4]
            value, = struct.unpack('I', excerpt)
            if lower <= value <= upper:
                print hex(i), value

        print '-' * 20

    dump(data, 0xefc55c)
    dump(data, 0xefff48)

    print struct.calcsize('L')

if __name__ == '__main__':
    main()
