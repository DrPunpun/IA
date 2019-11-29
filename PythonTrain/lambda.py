#Lambda functions
import math
impar = lambda x : x%2==0
print(impar(2))
print(impar(3))

positivo = lambda x : x >= 0
print(positivo(-1))
print(positivo(1))

compare_abs = lambda x,y : abs(x) < abs(y)
print(compare_abs(-1, 1))

polar = lambda x, y : (math.sqrt(x**2+ y**2), math.atan2(y,x))
print(polar(4,5))