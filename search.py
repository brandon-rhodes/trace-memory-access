import struct

def int_bytes(n):
    return struct.pack('I', n)

if __name__ == '__main__':
    with open('gdb_record.out', 'rb') as f:
        data = f.read()

    # n = 886357 + 1
    n = 886357
    for i in range(n - 10, n + 10):
        count = data.count(int_bytes(i))
        print i, count, '*' * count
    n += 7
    pattern = int_bytes(n)
    step = struct.calcsize('I')
    print 'Step size:', step, ' Target:', hex(n)
    count = data.count(pattern)
    print 'Count:', count
    assert count == 1
    i = data.index(pattern)
    assert i % 4 == 0
    for j in range(i - 15 * step, i + 25 * step, step):
        excerpt = data[j:j + step]
        n, = struct.unpack('I', excerpt)
        if i == j:
            print '===>',
        print hex(j), hex(n)
