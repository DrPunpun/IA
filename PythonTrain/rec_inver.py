def rec_inver(li):
	if li ==[]:
		return li
	return rec_inver(li[1:]) + [li[0]]

a = [1,2,3]
print(rec_inver(a))