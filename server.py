import socket

content = 'Hello, world.'

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sock.bind(('127.0.0.1', 8001))
    sock.listen(1)
    while True:
        sc, sockname = sock.accept()
        sc.sendall('HTTP/1.1 200 OK\r\n'
                   'Content-Type: text/plain\r\n'
                   'Content-Length: {}\r\n'
                   '\r\n'
                   '{}'.format(len(content), content))
        sc.close()
