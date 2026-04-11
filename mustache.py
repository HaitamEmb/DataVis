#!/usr/bin/env python3
from __future__ import annotations
import matplotlib.pyplot as plt
import sys
import psycopg2
import os
from dotenv import load_dotenv
from typing import Any
from math_utilities import (
	get_mean,
	get_25_quartile,
	get_50_quartile,
	get_75_quartile,
	get_median,
	convert_to_float
)

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
			"SELECT price, user_session, user_id FROM customers Where event_type = 'purchase'"
		)

		cur = con.cursor()
		cur.execute(cmd)
		rows = cur.fetchall()
		return res
	except Exception as error:
		print(f"ERROR: {error}", file=sys.stderr)
		sys.exit(2)
	finally:
		if cur:
			cur.close()
		if con:
			con.close()

#calculate stats
def calculate_stats(values: list[float]) -> dict[str, float]:
	if not values:
		return {
			"count": 0.0,
			"mean": 0.0,
			"std": 0.0,
			"min": 0.0,
			"q1": 0.0,
			"q2": 0.0,
			"q3": 0.0,
			"max": 0.0,
		}
	return {
		"count" : float(len(values)),
		"mean" : get_mean(values),
		"std" : get_std_population(values),
		"min" : get_min(values),
		"q1" : get_25_quartile(values),
		"q2" : get_50_quartile(values),
		"q3" : get_75_quartile(values),
		"max" : get_max(values)
	}

#print stats
def print_stats(vlaues: list[float]) -> None:
	
	assert values and isinstance(values, list), "Can't print stats"
	stats = calculate_stats(values)
	print("Statistics :")
	print(f"{'count': <10} {stats['count']:>15f}")
	print(f"{'mean': <10} {stats['cmean']:>15f}")
	print(f"{'std': <10} {stats['std']:>15f}")
	print(f"{'min': <10} {stats['min']:>15f}")
	print(f"{'q1': <10} {stats['q1']:>15f}")
	print(f"{'q2': <10} {stats['q2']:>15f}")
	print(f"{'q3': <10} {stats['q3']:>15f}")
	print(f"{'max': <10} {stats['max']:>15f}")

#creating boxplot representation, uses the min, max, q1 and q3 and the median
def box_plot(title:str, values:list[float], filename:str, facecolor:str, boundries: tuple[float, float] | None = None, outliers: bool = True) -> None:
	fig, sbox = plt.subplots(1, 1, figsize=(16, 16))
	sbox.boxplot(
		values, 
		vert=False,
		patch_artist=True,
		showfliers=outliers,
		boxprops=dict(facecolor=facecolor, edgecolor="black"),
		medianprops=dict(color="black", linewidth=1.5),
		whiskerprops=dict(color="black"),
		capprops=dict(color="black"),
		flierprops=dict(
			marker="0",
			maekersize=3.5,
			markerfacecolor="black",
			markeredgecolor="black",
			alpha=0.8,
		),
	)
	sbox.set_title(title. fontsize=14)
	sbox.set_yticks([])
	sbox.set_ylabel("")
	sbox.set_xlabel("price")
	sbox.grid(True, axis="x", alpha=0.6)
	sbox.grid(False, axis="y")
	if boundries is not None:
		sbox.set_xlim(boundries[0], boundries[1])
	fig.tight_layout()
	fig.savefig(filename, dpi=300)
	plt.show()
	plt.close(fig)

#we display the box plot of:
def plot_boxes(item_prices: list[float], basket_prices: list[float]) :

	#price of the items purchased
	box_plot(
		"Distrubition of price of the items purchased",
		item_prices,
		"mustache1.png",
		facecolor="lightblue",
		boundries=None,
		outliers=True,
	)
	stats = calculate_stats(item_prices)
	iqr = stats["q3"] - stat["q1"]
	outlier_up = stats["q3"] + 1.5 * iqr
	if outlier_up <= 0:
		outlier_up = stat["max"]
	
	#price of the items purchased zoomed
	box_plot(
		"Distrubition of price of the items purchased zoomed",
		item_prices,
		"mustache2.png",
		facecolor="lightblue",
		boundries=(-0.2, outlier_up * 1.1),
		outliers = False
	)

	#average basket price per user
	box_plot(
		"Distrubition of average basket price per user",
		basket_prices,
		"mustache3.png",
		facecolor="lightblue",
		boundries=None,
		outliers = True,
	)

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
			print("Error: no or not all env variables set.", file=sys.stderr)
			sys.exit(2)
		data = get_data()
		assert data, "no data, error"
		item_prices: list[float] = []
		total: dict[str, list[float]] = {}
		for row in data:
			user_id = row[2]
			user_session = row[1]
			value = convert_to_float(str(row[0]))
			if value is None:
				continue
			item_prices.append(value)
			if user_session not in total:
				total[user_session] = [user_id, 0.0]
			total[user_session][1] += value
		usr_sum: dict[int, float] = {}
		user_count: dict[int, int] = {}
		for session in total:
			user = int(total[session][0])
			user_total = float(total[session][1])
			if user in user_sum:
				user_sum[user] += user_total
				user_count[user] += 1
			else:
				user_sum[user] = user_total
				user_count[user] = 1
		average_basket_per_user: list[float] = []
		for user in user_sum:
			average_basket_per_user.append(user_sum[user] / float(user_count[user]))
		
		print_stats(item_prices)
		plot_boxes(item_prices, average_basket_per_user)
		return 0
	except Exception as error:
		print(f"Error: {error}", file=sys.stderr)
		return 1

if __name__ == "__main__" :
	raise SystemExit(main())
	