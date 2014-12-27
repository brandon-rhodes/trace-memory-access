from os import chdir

token = object()
list1 = [token] * 886000
for i in range(357):
    list1.append(token)

chdir('.')

list1.append(token)
list1.append(token)
list1.append(token)
list1.append(token)
list1.append(token)
list1.append(token)

chdir('.')
