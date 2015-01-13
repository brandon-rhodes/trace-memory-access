import posix
from _socket import socket, AF_INET, SOCK_STREAM

MAGIC = 0x1234566

def main():
    hash(MAGIC + 1)

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((b'127.0.0.1', 8001))
    data = b''
    while b'\r\n\r\n' not in data:
        data += s.recv(8192)
    heading, content = data.split(b'\r\n\r\n', 1)
    lines = heading.splitlines()
    version, status, text = lines[0].split()
    headers = dict(line.split(b': ', 1) for line in lines[1:])

    hash(MAGIC + 2)
    posix._exit(42)

    print(headers)

if __name__ == 'encodings' or __name__ == '__main__':
    main()
