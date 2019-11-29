def comp(li):
	if li == []:
		return 0
	return 1 + comp(li[1:])

a = []
for i in range(100):
	a.append(i)
print(comp(a))