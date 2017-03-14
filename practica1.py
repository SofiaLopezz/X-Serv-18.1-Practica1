#!/usr/bin/python3

#Sofia Lopez

import webapp
import csv
import os


class shortenUrlApp (webapp.webApp):
	Dict_Urls_Short = {}
	Dict_Urls = {}
	index = -1

	def writeURL(self, longURL, shortURL):
		with open("fich.csv", "a") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow([int(shortURL)] + [longURL])
		return None

	def readDict(self, file):
		with open("fich.csv", "r") as csvfile:
			if os.stat('fich.csv').st_size == 0:
				print("Empty file")
			else:
				reader = csv.reader(csvfile)
				for row in reader:
					self.Dict_Urls_Short[row[1]] = int(row[0])
					self.Dict_Urls[int(row[0])] = row[1]
					self.index = self.index+1
				return None
	
	def parse(self, request):
		recurso = request.split(' ', 2)[1]
		metodo = request.split(' ', 2)[0]

		if metodo == "POST":
			cuerpo = request.split('\r\n\r\n', 1)[1]
			cuerpo = cuerpo.split("=")[1].replace("+", " ")
		elif metodo == "GET":
			cuerpo = ""

		return (metodo, recurso, cuerpo)

	def process(self, resourceName):

		(metodo, recurso, cuerpo) = resourceName
		formulario = '<form action="" method="POST">'
		formulario += 'Get URL shorter: <input typr="text" name=valor"valor">'
		formulario += '<input type="submit" value="Enviar">'
		formulario += '</form>'

		if len(self.Dict_Urls_Short) == 0:
			self.readDict('fich.csv')
		if metodo == "GET":
		#Envio del formulario solicitado
			if recurso == "/":
				httpCode = "200 OK"
				htmlBody = "<html><body>" + formulario\
							+ "<p>" + str(self.Dict_Urls_Short)\
							+ "</p></body></html>"

			else:
				try:
					recurso = int(recurso[1:])
					if recurso in self.Dict_Urls:
						httpCode = "300 Redirect"
						htmlBody = "<html><body><meta http-equiv='refresh'"\
									+ "content='1 url="\
									+ self.Dict_Urls[recurso] + "'>"\
									+ "</p>" + "</body></html>"
					else:
						httpCode = "404 Not Found"
						htmlBody = "<html><body>"\
						+ "Error: Recurso no disponible"\
						+ "</body></html>"

				except ValueError:
					httpCode = "404 Not Found"
					htmlBody = "<html><body>"\
					+ "Error: Recurso no disponible"\
					+ "</body></html>"
					
				
		elif metodo == "POST":
			if cuerpo == "":
				httpCode ="404 Not Found"
				htmlBody = "<html><body>"\
							+ "Error: url vacía"\
							+ "</body></html>"
				return(httpCode, htmlBody)
			elif cuerpo.find("http") == -1:
				cuerpo = "http://" + cuerpo
				while cuerpo.find("%2F") != -1:
					cuerpo = cuerpo.replace("%2F", "/")

			else:
				cuerpo = cuerpo.split("%3A%2F%2F")[0]\
					+ "://" + cuerpo.split("%3A%2F%2F")[1]
				while cuerpo.find("%2F") != -1:
					cuerpo = cuerpo.replace("%2F", "/")

			if cuerpo in self.Dict_Urls_Short:
				index = self.Dict_Urls_Short[cuerpo]
			else:
				self.index = self.index + 1
				index = self.index

			self.Dict_Urls_Short[cuerpo] = index
			self.Dict_Urls[index] = cuerpo
			self.writeURL(cuerpo, index)
			httpCode = "200 OK"
			htmlBody = "<html><body>"\
						+ "<a href=" + cuerpo + ">" + cuerpo + "</href>"\
						+ "<p><a href=" + str(index) + ">" + str(index)\
						+ "</href></body></html>"

		else:
			httpCode = "404 Not Found"
			htmlBody = "<html><body>No soportado</body></html>"

		return (httpCode, htmlBody)

if __name__ == "__main__":
	try:
		testWebApp = shortenUrlApp("localhost", 1234)
	except KeyboardInterrupt:
		print ("")
		print ("Finish...")
