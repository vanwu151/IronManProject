l1 = [1 ,4 ,5, 6, 9]
index = [0, 2, 0, 4, 2, 4, 4, 0, 1, 3, 3]
l2 = []
for i in index:
    l2.append(str(l1[i]))
tel = ''.join(l2)
print('Tel：' + tel)