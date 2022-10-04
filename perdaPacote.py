#Relação sinal ruído SNR
def calcularSNR(pr,ruido):
    import math
    if pr > ruido: 
    	return abs(pr-ruido)
    else: 
    	return 0	 	

#taxa de erro do bit    
def getBpskBer(snr):
    import math
    snr = snr ** 0.5 #math.sqrt(snr)
    ber = 0.5 * math.erfc(snr)
    return ber

#probabilidade de perda do pacote
def calcularPer(tamanhoPacote, ber):
    temp = ((1-ber)**tamanhoPacote)
    per = 1 - temp
    return per            
    
