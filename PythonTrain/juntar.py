def juntar(l1, l2):
	if len(l1) != len(l2):
		return None
	if l1 == []:
		return []
	a, b = l1[0], l2[0]
	return [(a,b)] + juntar(l1[1:], l2[1:])

li =juntar([1,2], [3,4])
print(li)