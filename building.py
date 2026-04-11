#!/usr/bin/env python3
from __future__ import annotations
import matplotlib.pyplot as plt
import sys
import psycopg2
import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from typing import Any
from math_utilities import convert_to_float, get_percentile, round_to_multiple

#we tasked to create two histograms, one for number of orders according to frequency
#another for money spent on the site by customers

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
			password=os.getenv("PGPASSWORD"),
		)

		# We create a cursor object to run SQL commands
		cur = con.cursor()

		# Run commands to select data by event_type
		cmd: str = "SELECT price, user_id FROM customers WHERE event_type = 'purchase'"
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
	print("df price", df['price'])
	result = df.groupby('user_id')['price'].agg(
		order_count_per_user='count',
		total_spend_per_user='sum'
	)
	freq: list[float] = []
	spend: list[float] = []

	freq = result["order_count_per_user"].tolist()
	spend = result["total_spend_per_user"].tolist()

	freq_upper_limit: float = get_percentile(freq, 0.99)
	spend_upper_limit: float = get_percentile(freq, 0.99)
	freq_max = round_to_multiple(freq_upper_limit, 5)
	spend_max = round_to_multiple(spend_upper_limit, 10)
	if freq_max < 10.0:
		freq_max = 10.0
	if freq_max >= 40.0:
		freq_max = 39.9
	if spend_max < 50.0:
		spend_max = 50.0
	if spend_max >= 210.0:
		spend_max = 209.9
	try:
		plt.style.use("whitegrid")
	except Exception:
		pass

	#using histogram to plot the charts
	plt.figure(figsize=(16, 9))
	plt.xlabel("frequency")
	plt.ylabel("customers")
	plt.hist(
		freq,
		bins=bins,
		range=(0.5, freq_max * 0.95),
		alpha=0.6,
		edgecolor="white",
		linewidth=1.0,
	)
	plt.xlim(-0.5, freq_max)
	plt.xticks(range(0, int(freq_max) + 1, 10))
	plt.tight_layout()
	plt.savefig("freq.png")
	plt.show()
	plt.close()

	#second chart spend.png
	plt.figure(figsize=(16, 9))
	plt.xlabel("spending")
	plt.ylabel("customers")
	plt.hist(
		freq,
		bins=bins,
		range=(-34, 240),
		alpha=0.6,
		edgecolor="white",
		linewidth=1.0,
	)
	plt.xlim(-45, spend_max + 50)
	plt.ylim(0, 42500)
	plt.yticks(range(0, 40001, 5000))
	plt.xticks(range(0, int(spend_max), 50))
	plt.savefig("spend.png")
	plt.show()
	plt.close()

def main() -> int:
	try:
		env_path = Path(__file__).resolve().parent / ".env"
		load_dotenv(
			dotenv_path=env_path
		)
		if (
			not os.getenv("POSTGRES_DB")
			or not os.getenv("POSTGRES_USER")
			or not os.getenv("PGPASSWORD")
		) :
			print("Error env variables must be set", file=sys.stderr)
			sys.exit(2)
		building(get_data(), 5)
		return 0
	except Exception as error:
		print(f"Error: {error}", file=sys.stderr)
		return 1

if __name__ == "__main__" :
	raise SystemExit(main())
