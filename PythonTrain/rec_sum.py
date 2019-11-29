def rec_sum(li):
	if li == []:
		return 0
	return li[0] + rec_sum(li[1:])

a = []
for i in range(100):
	a.append(i)
print(rec_sum(a) == sum(a))