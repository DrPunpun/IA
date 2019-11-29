def remove_e_conta(lista, x):
	if lista==[]:
		return lista, 0
	l, c = remove_e_conta(lista[1:], x)
	if lista[0] == x:
		return l, c+1
	else:
		return [lista[0]] + l, c

print(remove_e_conta([1,2,3,4,4,3,2,6], 4))