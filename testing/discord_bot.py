import datetime
import discord
import mysql.connector
token = 'ODc2Mzk1MTk1OTEzMTA1NDQ5.YRjcoQ.3eimYkCIBfew4C03rrLAI8M2lEc'

mydb = mysql.connector.connect(
	host="localhost",
	user="citybee",
	password="citybee",
	database="citybee"
)
mycursor = mydb.cursor()


client = discord.Client()

def main(count):
	begin_time = datetime.datetime.now()
	mainer(count)
	print(datetime.datetime.now() - begin_time)


def mainer(count):
#	counter = 5
	sql = 'select id, make, model, license_plate, country,first_seen from cars where first_seen IS NOT NULL order by first_seen desc, license_plate asc limit ' + str(count) + ';'
	mycursor.execute(sql)
	data = mycursor.fetchall()
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
		channel = client.get_channel(876396025877790731)
		await channel.send(notification + message)
		await client.close()
	client.run(token)

if __name__ == "__main__":
	main()
