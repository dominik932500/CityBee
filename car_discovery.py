import json
import mysql.connector
import requests
import time
import datetime
import discord_bot

mydb = mysql.connector.connect(
	host="localhost",
	user="xxx",
	password="xxx",
	database="xxx"
)
mycursor = mydb.cursor()

countries = ["lt", "lv", "ee"]

global count

def main():
	begin_time = datetime.datetime.now()
	car_discovery()
	print(datetime.datetime.now() - begin_time)

def car_discovery():

	current_cars = []
	count = 0
	for i in countries:															#Going though each country
		url = "https://backend.citybee." + i + "/api/CarsLive/GetCarsDetails"	#Building an API url for each country
		headers={'Client':'SelfService', 'Country':'LT'}						#Client header is required, otherwise no response

		resp = requests.get(url,headers=headers)								#curl

		ts = time.gmtime()
		first_seen = time.strftime("%Y-%m-%d %H:%M:%S", ts)						#Making a timestamp, which later will be used to add new cars to the DB

		data_import = json.loads(resp.content)									#Convering curl response to json format
		data_export = json.dumps(data_import, indent=2)							#Can be used for pretty print :)

		legacy = 0																#Legacy 0 means that the car was not decommissioned 
		cars_amount = len(data_import)
		for n in range(0, cars_amount):											#Going though each car in the json
			id = data_import[n]["id"]
			license_plate = data_import[n]["license_plate"]
			make = data_import[n]["make"]
			model = data_import[n]["model"]
			print(id, license_plate, make, model)
			current_cars.append(str(id))
			try:																#Using simple try to insert new cars into the DB
				sql = "INSERT INTO cars(id, first_seen, legacy) VALUES (%s, %s, %s)"
				val = (id, first_seen, legacy)
				mycursor.execute(sql, val)
				mycursor.execute("UPDATE cars SET license_plate=%s, make=%s, model=%s, country=%s WHERE id=%s", (license_plate, make, model, i.upper(), id))
				mydb.commit()
				print("row count", mycursor.rowcount)
				count = count + mycursor.rowcount								#If try clause worked, we increase the counter
				print(count)
			except Exception as e: pass # print(e)
		mydb.commit()
	if count > 0:																#If new cars were added - we post that to Discord
		discord_bot.main(count)
	car_legacy(current_cars)


def car_legacy(current_cars):													#This function tests if some cars were removed from the fleet
	all_cars = []
	print(len(current_cars))
	car_list_sql = 'SELECT id from cars;'
	mycursor.execute(car_list_sql)
	car_list_id = mycursor.fetchall()
	print("Total number of rows in table: ", mycursor.rowcount)
	for row in car_list_id:
		str(all_cars.append(str(row[0])))
	legacy_cars = list(set(all_cars) - set(current_cars))
	print(len(all_cars))
	print(len(current_cars))
	print(len(legacy_cars))

	try:
		legacy = '1'
		for i in legacy_cars:
#			print(i)
			legacy = '1'
			mycursor.execute("UPDATE cars SET legacy=%s WHERE id=%s", (legacy, i))
		mydb.commit()
		legacy = '0'
	except Exception as e: print(e)
	mydb.commit()


if __name__ == "__main__":
	main()
