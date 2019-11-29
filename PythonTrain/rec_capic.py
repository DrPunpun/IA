def rec_capic(word):
	if len(word) == 1:
		return True
	if len(word) == 2:
		return word[0] == word[1]
	return word[0] == word[-1] and rec_capic(word[1:-1])

w1 = 'abc'
w2 = 'aba'
print(rec_capic(w1))
print(rec_capic(w2))