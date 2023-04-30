#!/usr/bin/python3
import json
import mysql.connector
import requests
import time
import yaml
from pathlib import Path

p = Path(__file__)
script_pwd = p.parent.absolute()

with open(str(script_pwd) + "/config.yml") as f:
	config = yaml.load(f, Loader = yaml.FullLoader)

mydb = mysql.connector.connect(
	host = config["db"]["host"],
	user = config["db"]["user"],
	password = config["db"]["password"],
	database = config["db"]["database"]
)

mycursor = mydb.cursor()
changes = 0

countries = ["lt", "lv", "ee"]
#countries = ['lv'] ###for testing

for i in countries:
	print(i)
	url = "https://backend.citybee." + i + "/api/CarsLive/GetAvailableCars"
	headers={'Client':'SelfService', 'Country':'LT'}

	ts = time.gmtime()
	current_time = time.strftime("%Y-%m-%d %H:%M:%S", ts)

	resp = requests.get(url, headers=headers)

	data_import = json.loads(resp.content)
	data_export = json.dumps(data_import, indent=2)

	cars_amount = len(data_import)
	for n in range(0, cars_amount):
		id = str(data_import[n]["id"]) + i
		price = data_import[n]["price"]
		address = data_import[n]["address"]
		city = data_import[n]["city"]
		try:
			address = str(address[0:30].strip())
			city = str(city[0:20].strip())
		except:
			pass
		mycursor.execute("UPDATE cars SET price=%s, last_loc_address=%s, last_loc_city=%s, last_seen_date=%s, legacy=%s WHERE id=%s AND country=%s", (price, address, city, current_time, 0, id, i))
	mydb.commit()
#	print(mycursor.rowcount, "record inserted.")
changes = changes + mycursor.rowcount
