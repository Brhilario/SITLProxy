#converter binário negativo    
def binaryToDecimal(binary): 
      
    binary1 = int(binary) 
    tamanho = len(binary)-1
    
    decimal, i, n = 0, 0, 0
    while(i <=  tamanho): 
        dec = binary1 % 10
        if tamanho == i and dec == 1 :
        	decimal = decimal - dec * pow(2, i)
        else:
        	decimal = decimal + dec * pow(2, i)	 
        binary1 = binary1//10
        i += 1
    return decimal

#formatar a coordenada     
def coordenadas(coordenada):
	if coordenada.count("-") == 1:		
		if len(coordenada) == 10:
			coordenada2 = coordenada[0:3]+"."+coordenada[3:]
		else: 
			coordenada2 = coordenada[0:4]+"."+coordenada[4:]
	else:
		if len(coordenada) == 9:
			coordenada2 = coordenada[0:2]+"."+coordenada[2:]
		else:
			coordenada2 =  coordenada[0:3]+"."+coordenada[3:]
	return coordenada2	
