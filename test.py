from os import _exit
import socket

token = object()
list1 = [token] * 886357
list2 = [token] * 333539

socket.socket()

# import sys
# print sys.getrefcount(token)
list3 = [token]

_exit(0)
