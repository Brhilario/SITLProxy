import csv
fieldnames = ["PR", "SNR", "BER", "PER", "ANGULO", "DISTANCIA", "TEMPO", "LATITUDE", "LONGITUDE"]
def criarArquivo(nome, pr, snr, ber, per, angulo, distancia, tempo, latitude, longitude):

	with open(nome+'.csv', 'a', newline='') as csvfile:
		
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writerow({"PR": pr[:3], "SNR":snr[:2], "BER":ber, "PER":per[:2], "ANGULO":angulo, "DISTANCIA":distancia, "TEMPO":tempo[:7], "LATITUDE":latitude[:10], "LONGITUDE":longitude[:10]})
		

