import math as mat
import binascii
import socket, select    
import socket
import sys
from geopy.distance import geodesic
import configparser
import random
import numpy as np
import utils
import perdaPacote as perda
import modelos 
import dados
import datetime


param = sys.argv[1:]
print('PARAMETRO', param)


HOSTS = '127.0.0.1'     # Endereco IP do Servidor
PORTS = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOSTS, PORTS)
tcp.bind(orig)
tcp.listen(5)
clientsock, clientaddr = tcp.accept()


HOST = '127.0.0.1'     # Endereco IP do drone
PORT = 5760            # Porta do drone
tcpD = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcpD.connect(dest)

inputs = [clientsock, tcpD]

#arquivo ini 
cfg = configparser.ConfigParser()
cfg.read('config.ini')
ganhoAntena = cfg.getint('section1', 'GanhoAntena')
potenciaAnt= cfg.getint('section1', 'Potencia')
comprimentoOnda = cfg.getfloat('section1','ComprimentoOnda')
ruido = cfg.getint('section1', 'Ruido')
expoentePerda = cfg.getfloat('section1','expoentePerda') 
distanciaRef = cfg.getint('section1', 'distanciaRef')
potenciaRef = cfg.getfloat('section1','potenciaRef') 
modeloProgacao = cfg.getint('section1', 'modeloProgacao') 
alfa0 = cfg.getfloat('section1','alfa0') 
alfa1 = cfg.getfloat('section1','alfa1') 
beta = cfg.getfloat('section1','beta') 
distanciaArquivo = 10
startTime = 0
aleatorio = 0
per = 0.0

#classe para guardar o posicionamento
class globalPosition:
	def __init__(self,  latitude, longitude, altura, altRelativa, vx, vy, vz):
		
		self.latitude = latitude
		self.longitude = longitude
		self.altura = altura
		self.altRelativa = altRelativa
		self.vx = vx
		self.vy = vy
		self.vz = vz	
		

			
		
while 1:
        infds, outfds, errfds = select.select(inputs, [], [], 5)
        estacaoBase = globalPosition(param[0], param[1], param[2], param[3], param[4], param[5], param[6])
        latDec = ''
        longDec = ''
        alturaDec = ''
        
        modelo = ''
        
        print("Estacao base:")
        print('Latitude: ', estacaoBase.latitude)
        print('Longitude: ', estacaoBase.longitude)
        print('Altura: ', estacaoBase.altRelativa)
        print('config', ganhoAntena)
        
        if len(infds) != 0:
                #print 'enter infds'    
                for fds in infds:
                        if fds is clientsock:

                                data = clientsock.recv(1024)
                                i = 1
                                posicao = 0

                                datahex = bytearray(data).hex()
                                
                                bytestring = format(int(datahex, 16), "b")
                                info = [bytestring[i:i+8] for i in range(0,len(bytestring),8)]
                                aleatorio = random.random()
                                if aleatorio > per:
                                	tcpD.send(data)

                        else:
                                i = 1
                                posicao = 0
                                data = tcpD.recv(1024)
                                datahex = bytearray(data).hex()
                                bytestring = format(int(datahex, 16), "b")
                               
                                info = [bytestring[j:j+8] for j in range(0,len(bytestring),8)]
                         

                                if len(info) > i:
                                	payload = info[i] 
                                	tamanhoPayload = int(payload,2)
                                if i == 1:
                                	if len(info) > 9:
                                		mensagemid = int(info[i+8]+info[i+7]+info[i+6],2)
                                	posicao = i+9+tamanhoPayload+2+1
                                print(posicao)
                                print(len(info))	
                                if posicao < len(info):		
                                	payload2 = info[posicao]
                                	#print('payload2', payload2)
                                	tamanhoPayload2 = int(payload2,2)
                                	if len(info) > 231:
                                		mensagemid2 = int(info[posicao+8]+info[posicao+7]+info[posicao+6],2)
                                		if mensagemid2 == 33:
                                			print('posicao:', posicao)
                                			if len(info) > 50:
                                				time = info[posicao+12]+info[posicao+11]+info[posicao+10]+info[posicao+9]

                                				posicao = posicao+12
                                				print('POS AQUI:', posicao)
                                				if len(info) > 60:
                                					latitude = info[posicao+4]+info[posicao+3]+info[posicao+2]+info[posicao+1] 
                                					latDec=utils.coordenadas(str(utils.binaryToDecimal(latitude)))
                                					print('latitude Drone', latDec)

                                					posicao = posicao+4
                                				#if len(info) > 60:
                                					longitude = info[posicao+4]+info[posicao+3]+info[posicao+2]+info[posicao+1]
                                					longdec = utils.coordenadas(str(utils.binaryToDecimal(longitude)))
                                					print('coordenada longitude:', longdec)				
                                			
                                					posicao = posicao+4
                                					altura =  info[posicao+4]+info[posicao+3]+info[posicao+2]+info[posicao+1]
                                					alturaDec = utils.binaryToDecimal(altura) 
                                			
                               					posicao = posicao+4
                               					print('posicao aqui preciso saber', posicao)
                               					if len(info) > 68:
                               						alturaRelDrone =  info[posicao+4]+info[posicao+3]+info[posicao+2]+info[posicao+1]
                               						alturaRelDecDrone = utils.binaryToDecimal(alturaRelDrone)/1000
                               						if latDec != '' and longdec != '':
                               							drone = globalPosition(latDec, longdec , alturaDec, alturaRelDecDrone, 0, 0, 0)
                               			
                               			
                               							dronePosicao = (drone.latitude,drone.longitude)
                               							estacao = (estacaoBase.latitude,estacaoBase.longitude)
                               							distancia = geodesic(dronePosicao, estacao).meters 
                               							print('Distancia: ',distancia)
                               				
                               							print('Altura Drone: ', alturaRelDecDrone) 
                               			
                               							alturaRelativa = int(alturaRelDecDrone) - int(estacaoBase.altRelativa)
                               			
                               							print('Altura relativa: ', alturaRelativa)
                               							if alturaRelativa > 0: 
                               								distanciaTotal = (((alturaRelativa**2) + (distancia**2))**0.5)
                               							else:
                               				 				distanciaTotal = 1
                               							print('distancia total', distanciaTotal)
                               							print('distancia arquivo', distanciaArquivo)
                               							distanciaTotalInt = int(distanciaTotal)


                               							if modeloProgacao == 1:
                               						
                               								pr = modelos.frees(distanciaTotal, comprimentoOnda, potenciaAnt, ganhoAntena)
                               						
                               								modelo = 'frees'
                               							if modeloProgacao == 2:
                               								modelo = 'logdistance'
                               						
                               								pr = modelos.logDistance(distanciaTotal, potenciaAnt, expoentePerda, distanciaRef, potenciaRef)
                               							if modeloProgacao == 3:
                               								modelo = 'los'
                               						
                               								frees = modelos.frees(distanciaTotal, comprimentoOnda, potenciaAnt, ganhoAntena)
                               					
                               								los = modelos.Plos(distanciaTotal, alturaRelativa)
                               								pr = frees-los
                               							if modeloProgacao == 4:
                               								modelo = 'olos'
                               						
                               								frees = modelos.frees(distanciaTotal, comprimentoOnda, potenciaAnt, ganhoAntena)
                               								if alturaRelativa > 0:
                               									angulo = mat.degrees(mat.asin(alturaRelativa/distanciaTotal))
                               								else:
                               									angulo = 0	
                               								print('angulo',angulo)
                               								olos = modelos.POlos(angulo, alfa0, alfa1, beta)
                               								pr = frees-olos	
                               						
                               							print('*******'+modelo+'****')
                               							print(modelo, pr)
                               							snr = perda.calcularSNR(pr,ruido)
                               							print('AQUI AQUI PR', pr)
                               							print('SNR: ', snr)
                               							ber = perda.getBpskBer(snr)
                               							print('ber: ', np.format_float_scientific(ber, precision = 1, exp_digits=3))
                               							per = perda.calcularPer(len(info), ber)
                               							print('per: ', np.format_float_scientific(per, precision = 1, exp_digits=3))
                               							print('@@@@@@@@', distanciaTotalInt)
                               							print('$$$$$$$$',distanciaArquivo)
                               					
                               							#if distanciaTotalInt > distanciaArquivo:
                               							distanciaArquivo = distanciaArquivo+10
                               							if startTime == 0:
                               								starts = datetime.datetime.now()
                               								startTime = 1
                               							time = datetime.datetime.now() - starts	
                               							dados.criarArquivo(modelo, str(pr), str(snr), str(ber), str(per), '0', str(distanciaTotal), str(time), str(drone.latitude), str(drone.longitude))
                               							distanciaArquivo = distanciaArquivo+10
                               						

                               				
                               #termina				
                               				
                               				

                                aleatorio = random.random()
                                #clientsock.send(data)
                                if startTime == 1:
                                	time1 = datetime.datetime.now() - starts
                                else: time1 = 0	
                                	#dados.criarArquivo('erro', modelo, str(snr), str(ber), str(per), '1', str(distanciaTotal), str(time1))
                                if aleatorio > per:
                                	if modelo != '':
                                		dados.criarArquivo('erro', modelo, str(snr), str(ber), str(per), '1', str(distanciaTotal), str(time1), str(drone.latitude), str(drone.longitude))
                                	clientsock.send(data)
                                else:
                                	time1 = datetime.datetime.now() - starts
                                	dados.criarArquivo('erro', modelo, str(snr), str(ber), str(per), '0', str(distanciaTotal), str(time1), str(drone.latitude), str(drone.longitude))
                                             
                

print ('Para sair use CTRL+X\n')
32
