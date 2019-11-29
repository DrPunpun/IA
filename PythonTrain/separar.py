def separar(li):
	if li == []:
		return [], []
	a, b = li[0]
	la, lb = separar(li[1:])
	return [a]+la, [b]+lb

lista = [(1,2),(3,4)]
print(separar(lista))