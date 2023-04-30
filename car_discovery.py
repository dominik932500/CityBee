#!/usr/bin/python3
import json
import mysql.connector
import requests
import time
import datetime
import discord_bot
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

countries = ["lt", "lv", "ee"]
#countries = ['lv'] ###for testing

global count

def main():
	begin_time = datetime.datetime.now()
	car_discovery()
	print(datetime.datetime.now() - begin_time)

def car_discovery():
	current_cars = []
	new_license_plates = []
	count = 0
	for i in countries:
		print(i) #Country TAG
		url = "https://backend.citybee." + i + "/api/CarsLive/GetCarsDetails"
		headers = {'Client':'SelfService', 'Country':'LT'}

		resp = requests.get(url, headers=headers)

		ts = time.gmtime()
		first_seen = time.strftime("%Y-%m-%d %H:%M:%S", ts)

		data_import = json.loads(resp.content)
		data_export = json.dumps(data_import, indent=2)

		legacy = 0
		cars_amount = len(data_import)
#		cars_amount = 5
		for n in range(0, cars_amount):
			id = str(data_import[n]["id"]) + i
			license_plate = data_import[n]["license_plate"]
			make = data_import[n]["make"]
			model = data_import[n]["model"]
			print(id, license_plate, make, model)
			current_cars.append(id)
			try:
				sql = "INSERT INTO cars(id, first_seen, legacy) VALUES (%s, %s, %s)"
				val = (id, first_seen, legacy)
				mycursor.execute(sql, val)
				mycursor.execute("UPDATE cars SET license_plate=%s, make=%s, model=%s, country=%s WHERE id=%s", (license_plate, make, model, i.upper(), id))
				mydb.commit()
				print("row count", mycursor.rowcount)
				count = count + mycursor.rowcount
			except Exception as e: pass #print(e)

		now = datetime.datetime.now()
		if now.hour == 14:
			for n in range(0, cars_amount):
				id = str(data_import[n]["id"]) + i
				license_plate = str(data_import[n]["license_plate"])
				try:
					mycursor.execute("UPDATE cars SET license_plate=%s WHERE id=%s AND COUNTRY=%s", (license_plate, id, i.upper()))
					if mycursor.rowcount > 0:
						updated_car_details = [id, license_plate]
						new_license_plates.append(updated_car_details)
				except Exception as e: print(e)
		mydb.commit()
		if len(new_license_plates) > 0:
			discord_bot.license_plate(new_license_plates, i)
	if count > 0:
		discord_bot.main(count)

	car_legacy(current_cars)


def car_legacy(current_cars):
	all_cars = []
	current_cars.sort()
	car_list_sql = 'SELECT id from cars;' # where country = "LT";'
	mycursor.execute(car_list_sql)
	car_list_id = mycursor.fetchall()
	for row in car_list_id:
		str(all_cars.append(str(row[0])))
	legacy_cars = list(set(all_cars) - set(current_cars))
	legacy_cars.sort()
	try:
		legacy = '1'
		for i in legacy_cars:
			legacy = '1'
			mycursor.execute("UPDATE cars SET legacy=%s WHERE id=%s", (legacy, i))
			if mycursor.rowcount > 0:
				discord_bot.legacy_cars(i)
		mydb.commit()
		legacy = '0'
	except Exception as e: print(e)
	mydb.commit()

if __name__ == "__main__":
	main()
