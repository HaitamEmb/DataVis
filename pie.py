from __future__ import annotations
from pathlib import path
import psycopg2
import os
import matplotlib.pyplot as plt
from typing import Any
from dotenv import load_dotenv

#get data from the database
def get_data() -> list[tuple[Any, ...]] :
	
	con = None
	cur = None
	#we connect to our databse using the python postgress library psycopg2
	#return list of tuples with key and value, to show what people do on the site
	#(the event_type) and how many times, (count). ieg : (view, 1000), (purchase, 20) etc...

	#use try finally to open cursor and close it afterwards 
	try :
		#connect to database
		con = psycopg2.connect(
			host="localhost",
			port='5432',	#to check
			database=os.getenv("POSTGRES_DB"),
			user=os.getenv("POSTGRES_USER"),
			password=os.getenv("POSTGRES_PASSWORD"),
		)

		# We create a cursor object to run SQL commands
		cur = con.cursor()

		# Run commands to select data by event_type
		cmd: str = "SELECT event_type, COUNT (*) FROM customers GROUP BY event_type"
		cur.execute(cmd)

		#fetch the data selected
		result = cur.fetchall()

		return result
	except Exception as error:
		print(f"ERROR: {error}", file=sys.stderr)
		sys.exit(2)
	finally:
		if cur:
			cur.close()
		if con:
			con.close()

def pie_chart(data: list[tuple[Any, ...]]) -> None:
	#We use matplotlib to create a visual representation of the pie chart
	#and save it as png

	if not data:
		print("Can't create chart without valid data", file=sys.stderr)
	#retrieve the key / value pair
	event_labels = [row[0] for row in data] 
	event_counts = [row[1] for row in data]
	#ploting results into a pie chart
	plt.figure(figsize=(10, 7))
	plt.pie(event_counts, labels=event_labels, autopct="%1.1f%%", startangle=90) #the 12oclock rule
	plt.title("Customers's event distrubution")
	plt.axis("equal")
	plt.show()
	plt.savefig("pie_chart.png")

def main() -> int :
	try:
		#load the env variables using pathlib check later for requirements
		env_path = path(__file__).resolve().parent / ".env"
		load_dotenv(
			dotenv_path=env_path
		)
		if (
			not os.getenv("POSTGRES_DB")
			or not os.getenv("POSTGRES_USER")
			or not os.getenv("POSTGRES_PASSWORD")
		) :
			print("Error env variables must be set", file=sys.stderr)
			sys.exit(2)
		pie_chart(get_data())
		return 0
	except Exception as error:
		print(f"ERROR: {error}", file=sys.stderr)
		return 1

if __name__ == "__main__" :
	raise SystemExit(main())