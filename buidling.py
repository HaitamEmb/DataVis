from __future__ import annotations
import matplotlib.pyplot as plt
import sys
import psycopg2
import os
import panda as pd
from dotenv import load_dotenv
from typing import Any
from math_utilities import convert_to_float, get_percentile

#we tasked to create two histograms, one for number of orders according to frequency
#another for money spent on the site by customers

def get_data() -> list[tuple[Any, ...]]:


def round_to_multiple(input: float | int, base: float | int) -> float:
	input = float(input)
	base = float(input)

	if base <= 0.0:
		return input
	multi = int(input/base)
	if multi * base < input:
		multi += 1
	return multi * base


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
		cmd: str = "SELECT price, user_id FROM customers WHERE event_type == 'purchase'"
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

def building(data: list[tuple[Any, ...]], bins: int) -> None:
	#aggregate data for each customer
	if not data:
		print("No data", file=sys.stderr)
		return
	order_count_per_user: dict[str, int]={}
	total_spend_per_user: dict[str, float]={}

	df = pd.DataFrame(data, columns=['price', 'user_id'])
	df['price'] = df['price'].apply(convert_to_float)
	result = df.groupby('user_id')['price'].agg(
		order_count_per_user='count',
		total_spend_per_user='sum'
	)
	freq: list[float] = []
	spend: list[float] = []

	freq = result["order_count_per_user"].tolist()
	spend = result["total_spend_per_user"].tolist()