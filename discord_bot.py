#!/usr/bin/python3
import datetime
import discord
import mysql.connector
import yaml
from discordwebhook import Discord
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

token = config["discord"]["token"]

client = discord.Client(intents=discord.Intents.default())

def main(count):
	begin_time = datetime.datetime.now()
	mainer(count)
	print(datetime.datetime.now() - begin_time)
#	license_plate()

def license_plate(new_license_plates, country):
	channel_plates_webhook = config["discord"]["channel_plates_webhook"]
	old_plate = old_make = old_model = old_country = ''
	for n in range(0, len(new_license_plates)):
		new_plate = new_license_plates[n][1]
		id = str(new_license_plates[n][0])
		mycursor.execute("select id, license_plate, make, model, country from cars_import WHERE id=%s AND COUNTRY=%s", (id, country))
		data = mycursor.fetchall()
		for row in data:
			old_plate = row[1]
			old_make = row[2]
			old_model = row[3]
			old_country = row[4]
		message = old_make + ' ' + old_model + ' ' + old_country + ' ' + old_plate + ' > ' + new_plate
		if old_plate.strip() != new_plate.strip():
			message_sender(message, channel_plates_webhook)
			print(message)

def legacy_cars(legacy_id):
	channel_legacy_webhook = config["discord"]["channel_legacy_webhook"]
	sql = 'select id, license_plate, make, model, country from cars WHERE id = "' + legacy_id + '";'
	mycursor.execute(sql)
	data = mycursor.fetchall()
	for row in data:
		legacy_plate = row[1]
		legacy_make = row[2]
		legacy_model = row[3]
		legacy_country = row[4]
	message = legacy_make + ' ' + legacy_model + ' ' + legacy_plate + ' ' + legacy_country
	message_sender(message, channel_legacy_webhook)

def message_sender(message, webhook):
	discord = Discord(url=webhook)
	discord.post(content=message)

def mainer(count):
#	counter = 5
	sql = 'select id, make, model, license_plate, country,first_seen from cars where first_seen IS NOT NULL order by first_seen desc, license_plate asc limit ' + str(count) + ';'
	mycursor.execute(sql)
	data = mycursor.fetchall()
	channel_id = int(config["discord"]["channel_id"])
#	print("Total number of rows in table: ", mycursor.rowcount)
	data_id = []
	data_make = []
	data_model = []
	data_license_plate = []
	data_country = []
	data_date_added = []
	for row in data:
		str(data_id.append(str(row[0])))
		str(data_make.append(str(row[1])))
		str(data_model.append(str(row[2])))
		str(data_license_plate.append(str(row[3])))
		str(data_country.append(str(row[4])))
		str(data_date_added.append(str(row[5])))

	notification = 'New cars were added!\n'
	message = ''

	for i in range(0, len(data_id)):
		message = str(message) + ' ' + data_id[i] + ' ' + data_make[i] + ' ' + data_model[i] + ' ' + data_license_plate[i] + ' ' + data_country[i] + ' ' + data_date_added[i] + "\n"
	print(message)

	@client.event
	async def on_ready():
		print('We have logged in as {0.user}'.format(client))
		channel = client.get_channel(channel_id)
		await channel.send(notification + message)
		await client.close()
	client.run(token)

if __name__ == "__main__":
	main()
