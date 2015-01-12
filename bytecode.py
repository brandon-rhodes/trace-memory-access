import dis
import sys

if __name__ == '__main__':
    if sys.version_info[:2] != (3, 4):
        print('Error: wrong version of Python')
        exit(1)
    from target import main
    dis.dis(main)
