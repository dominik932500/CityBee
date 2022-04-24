import json
import mysql.connector
import requests
import glob

mydb = mysql.connector.connect(
	host="localhost",
	user="citybee",
	password="citybee",
	database="citybee"
)
mycursor = mydb.cursor()

import_pwd = '/home/pi/program/citybee/import/*'

countries = ["lt", "lv", "ee"]
files_list = sorted(glob.glob(import_pwd))
##files_list = ['/home/pi/program/citybee/import/carlist_LT_2019-10.txt']

for i in files_list:
	print(i)
	with open(i) as f:
		car_list = f.readlines()
	car_list = [x.strip() for x in car_list]
#	print(car_list)
	for l in car_list:
#		print(l)
		car_info = l
		car_details = car_info.split(",")
		try:
#		for j in range(0, len(car_details)):
#				print(car_details[j])
			id = car_details[0]
			license_plate = car_details[1].strip()
			make = car_details[2].strip()
			model = car_details[3].strip()
			print(id, license_plate, make, model)
			sql = "INSERT INTO cars(id, license_plate, make, model) VALUES (%s, %s, %s, %s)"
			val = (id, license_plate, make, model)
			mycursor.execute(sql, val)
			mydb.commit()
			print(mycursor.rowcount, "record inserted.")
		except:
			pass

#Ufor i in countries:

#		try:
#			sql = "INSERT INTO cars(id, license_plate) VALUES (%s, %s)"
#			val = (id, license_plate)
#			mycursor.execute(sql, val)
#			mydb.commit()
#		except:
#			pass
#		mycursor.execute("UPDATE cars SET license_plate=%s, make=%s, model=%s, country=%s WHERE id=%s", (license_plate, make, model, i.upper(), id))
#		mydb.commit()
#		print(mycursor.rowcount, "record inserted.")
