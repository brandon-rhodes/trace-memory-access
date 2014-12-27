import struct

def int_bytes(n):
    return struct.pack('I', n)

def main():
    with open('gdb_record.out', 'rb') as f:
        data = f.read()

    n = 886357

    if True:
        lower = n - 10
        upper = n + 10

        for i in range(0, len(data), 4):
            excerpt = data[i:i+4]
            value, = struct.unpack('I', excerpt)
            if lower <= value <= upper:
                print hex(i), value

        print '-' * 20

    return

    for i in range(n - 10, n + 10):
        count = data.count(int_bytes(i))
        print i, count, '*' * count

    print

    pattern = int_bytes(886359)
    i = -1
    while True:
        old_i = i
        i = data.find(pattern, i + 1)
        if i == -1:
            break
        if old_i != -1:
            print '+', i - old_i, '=',
        print hex(i)

    return

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

if __name__ == '__main__':
    main()
