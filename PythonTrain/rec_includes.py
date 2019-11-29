def rec_includes(li, v):
	if li ==[]:
		return False
	return li[0]==v or rec_includes(li[1:], v)

a = []
for i in range(100):
	a.append(i)
print(rec_includes(a, 50))
print(rec_includes(a, 100))