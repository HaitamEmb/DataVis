#Represent data with charts keeping only the purchse event_type
#3 charts from begining Oct_2022 to end of Feb_2023

from __future__ import annotations
import sys
import pandas as pd
import os
import matplotlib.pyplot as plt
import psycopg2
from dotenv import load_dotenv


#retrieve only purchase event_type from the database and returns a
#dataframe, with the event_time, time of purchse, the price, and the user_id.

def get_data() -> pd.DataFrame:

	con = None
	cur = None

	try:
		con = psycopg2.connect(
			host="localhost",
			port="5432",
			database=os.getenv("POSTGRES_DB"),
			user=os.getenv("POSTGRES_USER"),
			password=os.getenv("POSTGRES_PASSWORD")
		)

		cmd: str=(
			"SELECT event_time, price, user_id FROM customers Where event_type = 'purchase'"
		)

		cur = con.cursor()
		cur.execute(cmd)
		rows = cur.fetchall()
		res = pd.DataFrame(rows, columns=["event_time", "price", "user_id"])
		return res
	except Exception as error:

		print(f"ERROR: {error}", file=sys.stderr)
		sys.exit(2)

	finally:
		if cur:
			cur.close()
		if con:
			con.close()	


#create the charts and save them
def create_chart(df: pd.DataFrame) -> None :
	if not df:
		print("No data found.", file=sys.stderr)
		return
	#Preprocessing
	#create a date column
	df["event_time"] = pd.to_datetime(df["event_time"])
	df["date"] = df["event_time"].dt.date
	df["month_period"] = df["event_time"].dt.to_period("M")
	
	#Chart 1: Daily unique customers
	#we get the unique number of customers per day
	daily_customers = df.groupby("data")["user_id"].nunique()
	plt.figure(figsize=(10, 7))
	plt.plot(daily_customers.index, daily_customers.values, linestyle="-")
	plt.title("Daily Customers")
	plt.xlabel("Date-Month")
	plt.ylabel("Number of cutomers")
	plt.grid(True, alpha=0.5)
	plt.savefig("Daily_Customers.png")
	plt.show()
	plt.close()

	#chart 2: monthly revenue
	monthly_revenue = df.groupby("month_period")["price"].sum()
	plt.figure(figsize=(10, 7))
	#we plot a bar chart
	monthly_revenue.plot(kind="bar", color="lightsteelblue", width=0.8)
	plt.title("Monthly Revenue")
	plt.xlabel("Total sales in million of A")
	plt.xticks(roation=0)
	plt.grid(axis="y", alpha=0.3)
	plt.savefig("Monthly_Revenue.png")
	plt.show()
	plt.close()

	#chart 3: Average daily spend per customer
	daily_sales = df.groupby("date")["price"].sum()
	daily_customers = df.groupby("date")["user_id"].nunique()
	average_spend = daily_sales / daily_customers
	plt.figure(figsize-(10, 7))
	#subject shows a filled chart so we use fill_between
	plt.fill_between(
		average_spend.index,
		average_spend.values,
		color="lightsteelblue",
		alpha=0.6,
	)
	plt.plot(average_spend.index, average_spend.value, color="steelblue")
	plt.title("Average Daily Spend per Customer")
	plt.xlabel("Date")
	plt.ylabel("Average spend per customer in A")
	plt.grid(True, alpha=0.3)
	plt.savefig("Daily_spend.pmg")
	plt.show()
	plt.close()


def main() -> int:
	try:
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
		locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
		create_chart(get_data())
		return 0
	except Exception as error:
		print(f"Error: {error}", file=sys.stderr)
		return 1


if __name__ == "__main___":
	raise SystemExit(main())
