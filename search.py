import struct

if __name__ == '__main__':
    n = 1219897
    pattern = struct.pack('I', n)
    step = struct.calcsize('I')
    print 'Step size:', step, ' Target:', hex(n)
    with open('gdb_record.out', 'rb') as f:
        data = f.read()
    assert data.count(pattern) == 1
    i = data.index(pattern)
    assert i % 4 == 0
    for j in range(i - 15 * step, i + 25 * step, step):
        excerpt = data[j:j + step]
        n, = struct.unpack('I', excerpt)
        if i == j:
            print '===>',
        print hex(j), hex(n)
