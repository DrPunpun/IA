def rec_concat(l1, l2):
	if l2 == []:
		return l1
	l1.append(l2[0])
	return rec_concat(l1, l2[1:])

a = [1,2,3]
b = [2,3,4]
print(rec_concat(a, b))