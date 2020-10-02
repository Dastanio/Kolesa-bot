import os
import requests
from bs4 import BeautifulSoup as BS

class KolesaKz:
	host = 'https://kolesa.kz'
	url = 'https://kolesa.kz/cars'
	list_car_id = []
	list_car_id_file = ''

	def __init__(self, list_car_id_file):
		self.list_car_id_file = list_car_id_file

		if(os.path.exists(list_car_id_file)):
			self.list_car_id = list(map(lambda x: x.strip(), open(list_car_id_file, 'r').readlines()))
		else:
			open(list_car_id_file, 'w').write('')

	def new_cars(self):
		response = requests.get(self.url)
		html = BS(response.content, 'html.parser')

		cars = []
		items = html.findAll('div', class_='row vw-item list-item a-elem')

		for i in items:
			id_car = i['data-id']

			if id_car not in self.list_car_id:
				self.list_car_id.append(id_car)
				self.update_lastkey()

				cars.append('%s/a/show/%s' % (self.host, id_car))

		return cars

	def update_lastkey(self):
		with open(self.list_car_id_file, "w") as f:
			f.write('\n'.join(self.list_car_id))