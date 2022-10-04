import csv
fieldnames = ["PR", "SNR", "BER", "PER", "ANGULO", "DISTANCIA", "TEMPO", "LATITUDE", "LONGITUDE"]
def criarArquivo(nome, pr, snr, ber, per, angulo, distancia, tempo, latitude, longitude):

	with open(nome+'.csv', 'a', newline='') as csvfile:
		
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writerow({"PR": pr, "SNR":snr, "BER":ber, "PER":per, "ANGULO":angulo, "DISTANCIA":distancia, "TEMPO":tempo, "LATITUDE":latitude, "LONGITUDE":longitude})
		

