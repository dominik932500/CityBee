import json
import mysql.connector
import requests
import time

mydb = mysql.connector.connect(
	host="localhost",
	user="citybee",
	password="citybee",
	database="citybee"
)
mycursor = mydb.cursor()
changes = 0

countries = ["lt", "lv", "ee"]

for i in countries:
	print(i)
	url = "https://backend.citybee." + i + "/api/CarsLive/GetAvailableCars"
	headers={'Client':'SelfService', 'Country':'LT'}

	ts = time.gmtime()
	current_time = time.strftime("%Y-%m-%d %H:%M:%S", ts)

	resp = requests.get(url,headers=headers)

	data_import = json.loads(resp.content)
	data_export = json.dumps(data_import, indent=2)

	cars_amount = len(data_import)
	for n in range(0, cars_amount):
		id = data_import[n]["id"]
		price = data_import[n]["price"]
		address = data_import[n]["address"]
		city = data_import[n]["city"]

		try:
			address = str(address[0:30].strip())
			city = str(city[0:20].strip())
		except:
			pass

#		print(n, id, price, address, city)
#		print(price, address, city, current_time, id, i)

#id   | make          | model         | license_plate | country | last_loc_lat | last_loc_long | last_loc_address | last_loc_city | last_seen_date | first_seen | price
#id   | make          | model         | license_plate | country | last_loc_address                   | last_loc_city         | last_seen_date      | first_seen | price
		mycursor.execute("UPDATE cars SET price=%s, last_loc_address=%s, last_loc_city=%s, last_seen_date=%s WHERE id=%s AND country=%s", (price, address, city, current_time, id, i))
	mydb.commit()
#	print(mycursor.rowcount, "record inserted.")
changes = changes + mycursor.rowcount

#print(changes)
