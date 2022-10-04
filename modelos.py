import math as mat
#olos
def POlos(angulo, alfa0, alfa1, beta):
    ang = 90-angulo
    ang = ang/beta
    ang = mat.exp(ang)
    olos = alfa0 + alfa1*ang
    return olos

#los 
def Plos(distancia, altura):
    if altura > 0:	
    	los = altura / distancia 
    	los = -20 * (mat.log10(los))
    else:
    	los = 0	
    return los

#log Distance
def logDistance(distanciaTotal, potenciaAnt, expoentePerda, distanciaRef, potenciaRef):
    if distanciaTotal <= distanciaRef:
    	return potenciaAnt - potenciaRef
    pathLossDb = distanciaTotal / distanciaRef	
    pathLossDb = 10 * expoentePerda * (mat.log10(pathLossDb)) 
    rxc = - potenciaRef - pathLossDb    		
    return potenciaAnt + rxc
    

#free space
def frees(distanciaTotal, comprimentoOnda, potenciaAnt, ganhoAntena):
    pr =  (4 * 3.14159 * distanciaTotal)
    pr = comprimentoOnda / pr
    pr = 20 * (mat.log10(pr))
    pr = pr + potenciaAnt + ganhoAntena + ganhoAntena
    return pr
