from os import chdir

token = object()
list1 = [token] * 886357

chdir('.')

list1.append(token)
list1.append(token)
list1.append(token)

chdir('.')
