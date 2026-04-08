#Elbow graph, is used to determine the right K number for K-Means clustering.
#The K-means Clustering consists of finding the right number of clusters that
#the dataset should be "clusterd" to. We use an approach consisitng of randomly 
#choosing k points that acts as points of origin, then calculating the distance between
#each point and the each origin, the points then grouped to their nearest respective
#origins. We keep iterating and plot the inertia and find the elbow point or optimal K value

from __future__ import annotations
import random
from math_utilities import get_squared_distance, get_percentile, convert_to_float, get_mean, get_std_population, get_percentile
from typing import Any
import psycopg2
import matplotlib.pyplot as plt
import os
import sys



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



def score_normalization(vectors: list[tuple[float, float]]) -> list[tuple[float, float]] :
	
	freq: list[float] = []
	spend: list[float] = []
	for vector in vectors:
		freq.append(vector[0])
		spend.append(vector[1])
	freq_mean: float = get_mean(freq)
	spend_mean: float = get_mean(spend)
	freq_std: float = get_std_population(freq)
	spend_std: float = get_std_population(spend)
	if freq_std == 0.0:
		freq_std = 1.0
	if spend_std == 0.0:
		spend_std = 1.0
	z_vectors: list[tuple[float, float]] = []
	for vector in vectors:
		z_freq: float = (vector[0] - freq_mean) / freq_std
		z_spend: float = (vector[1] - spend_mean) / spend_std
		z_vectors.append((z_freq, z_spend))
	return z_vectors

def build_data(data: list[tuple[Any, ...]]) -> list[tuple[float, float]]:
	if not data:
		print("No data", file=sys.stderr)
		return
	customers_vec: list[tuple[float, float]] = []
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
	for i in range(len(freq)):
		customers_vec.append((float(freq[i]), float(spend[i])))
	return customers_vec
#we get the k-Means inertia by comuting the sum of squared errors
def get_kmeans(points: list[tuple[float, float]], k:int) -> float:
	#we need to randomly generate k points
	if k <= 0:
		return 0.0
	if k >= len(points):
		return 0.0
	#we choose a seed to randomize from, that ensures deterministic behaviour
	randomize = random.Random(42)
	random_points: list[tuple[float, float]] = points
	randomize.shuffle(random_points)
	origin_points: list[tuple[float, float]] = []
	origin_points_idx = 0
	#we determine the orig_pts by adding them to the list of origpts
	while origine_points_idx < k :
		origin_points.append(random_points[origin_points_idx])
		origin_points_idx += 1
	#we label each point close to the orig_pt respectively
	assignments: list[int] = [0] * len(points)
	i_idx = 0
	while i_idx < 25 : #thats K means max iteration number
		point_idx = 0
		while point_idx < len(points) :
			point = points[point_idx]
			closest_cluster_idx = 0
			closest_dist : float = get_squared_distance(point, origin_points[0])
			cluster_idx = 1
			while cluster_idx < k:
				current_dist = get_squared_distance(point, origin_points[cluster_idx])
				if current_dist < closest_dist:
					closest_dist = current_dist
					closest_cluster_idx = cluster_idx
				cluster_idx += 1
				assignments[point_idx] = closest_cluster_idx
				point_idx += 1
		#
		sum_x: list[float] = [0.0] * k
		sum_y: list[float] = [0.0] * k
		amount_per_cluster: list[int] = [0] * K
		point_idx = 0
		while point_idx < len(points):
			cluster_id: int = assignments[point_idx]
			sum_x[cluster_id] += points[point_idx][0]
			sum_y[cluster_id] += points[point_idx][1]
			amount_per_cluster[cluster_id] += 1
			point_idx += 1
		new_orig_pts: list[tuple[float, float]] = []
		cluster_idx = 0
		while cluster_idx < k:
			if amount_per_cluster[cluster_idx] == 0:
				new_orig_pts.append(random_points[randomize.randrange(0. len(random_points))])
			else :
				cx: float = sum_x[cluster_idx] / float(amount_per_cluster[cluster_idx])
				cy: float = sum_y[cluster_idx] / float(amount_per_cluster[cluster_idx])
				new_orig_pts.append((cx, cy))
			cluster_idx += 1
		i_idx += 1
		origin_points = new_orig_pts
	inertia_value: float = 0.0
	point_idx = 0
	while point_idx < len(points) :
		origin_point = origin_points[assignments[point_idx]]
		inertia_value += get_squared_distance(points{point_idx}, origin_point)
		point_idx += 1
	return inertia_value			
#the optimal k value is the point where the error starts leveling off
#to determine the k number we need to calculate the longest perpendicular distance between
#point in the graph and the line connecting between the head (1, inertia[1]) and tail (k, inertia[k]) of the graph.
def find_k_value(z_vectors: list[tuple[float, float]]) -> tuple[list[int], list[float], int]:
	
	#we get the x and y values and "draw the line"
	x_values: list[int] = []
	inertia_values: list[int] = []
	k = 1
	#I choose a K max to be 7
	while k <= 7:
		one_inertia_value = get_kmeans(z_vectors, k)
		#x 
		x_values.append(k)
		#y
		inertia_values.append(one_inertia_value)
		k += 1
	n = len(inertia_values)
	if n < 3:
		print("Error: invalid values", file=sys.stderr)
		sys.exit(3)
	#head and tail coordinates of the straight line
	head_x = float(x_values[0])
	tail_x = float(x_values[-1])
	head_y = float(inertia_values[0])
	tail_y = float(inertia_values[-1])
	#derivative of whole line
	line_dx = tail_x - head_x
	line_dy = tail_y - head_y
	line_len = (line_dx * line_dx + line_dy * line_dy) ** 0.5
	if line_len <= 0.0:
		print("Error: invalid values", file=sys.stderr)
		sys.exit(3)
	best_k_idx = 1
	#init the best distance
	best_distance = -1.0
	k_idx = 1
	while k_idx < n - 1:
		px = float(k_idx + 1)
		py = inertia_values[k_idx]
		distance = (abs(line_dy * px - line_dx * py + tail_x * head_y - tail_y * head_x) / line_len)
		if distance > best_distance:
			best_distance = distance
			best_k_idx = k_idx
		k_idx += 1
	return (x_values, inertia_values, best_k_idx + 1)

def plot_elbow(x_values: list[int], y_values: list[float], k: int) -> None:
	
	plt.figure(figsize=(16, 9))
	plt.plot(x_values, y_values)
	plt.xlabel("Number of clusters (k)")
	plt.ylabel("Inertia sse")
	plt.title("Elbow Method")
	plt.axvline(float(k), linestyle="-", alpha=0.6)
	plt.text(float(k) + 0.1, inertia_values[0] * 0.9, f"k = {k}")
	plt.xticks(k_values)
	plt.tight_layout()
	plt.savefig("elbow.png")
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
		data = get_data()
		customers_vec = build_data(data)
		norm_vectors = score_normalization(customers_vec)
		x_values, inertia_values, closest_k = find_k_value(norm_vectors)
		plot_elbow(x_values, inertia_values, closest_k)
		return 0
	except Exception as error:
		print(f"ERROR: {error}", file=sys.stderr)
		return 1
	
	if __name__ == "__main__":
		raise SystemExit(main())

	
