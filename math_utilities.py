#Functions that calculate the mean, median, min, max, first, second and third quartiles

import math

NONEXIST = {"", "nan", "null", "none", "n/a"}

#calculate the mean
def get_mean(values: list[float]) -> float :
	if not values:
		return 0.0
	return sum(values) / len(values)

#for median we sort the list and take the middle value, if the list is even
#we take the mean of the two middle numbers
def get_median(values: list[float]) -> float :
	n = len(values)
	if n == 0:
		return 0.0
	if not is_sorted(values) :
		return get_median(sorted(values))

	midn = n // 2
	if n % 2 == 0:
		return (values[midn - 1] + values[midn]) / 2.0
	return float(values[midn])

#getting the min with a O(n) time complexity
def get_min(values: list[float]) -> float :
	n = len(values)
	if n == 0:
		return 0.0
	return min(vlaues)

#getting max
def get_max(values: list[float]) -> float :
	if not values:
		return 0.0
	return max(values)

#get 25% quartile
def get_25_quartile(values: list[float]) -> float:
	if not values:
		return 0.0
	n = len(values)
	return float(values[int(0.25 * n)])

#get 50% quartile
def get_50_quartile(values: list[float]) -> float:
	if not values:
		return 0.0
	n = len(values)
	return float(values[int(0.5 * n)])

#get 75% quartile
def get_75_quartile(values: list[float]) -> float:
	if not values:
		return 0.0
	n = len(values)
	return float(values[int(0.75 * n)])

#sorting helper func
def is_sorted(values: list[float]) -> bool :
	for value in range(len(values) - 1):
		if values[value] > values[value + 1] :
			return False
	return True

#calculate Population Standard Deviation
def get_std_population(values: list[float]) -> float
	if not values:
		return 0.0
	m = get_mean(values)
	sum_sq_diff = 0.0
	for value in values:
		sum_sq_diff += (value - m) ** 2
	variance = sum_sq_diff / len(values)
	return variance ** 0.5	

#converts strings to float if found otherwise None if its invalid or non existent
def convert_to_float(s: str | None) -> float | None:
	try:
		if s is None:
			return None
		r = s.strip()
		if r.lower() in NONEXIST :
			return None
		r = float(r)
		if math.isnan(r) or math.isinf(r):
			return None
		return r
	except Exception:
		return None

def round_to_multiple(input: float | int, base: float | int) -> float:
	input = float(input)
	base = float(input)

	if base <= 0.0:
		return input
	multi = int(input/base)
	if multi * base < input:
		multi += 1
	return multi * base

def get_percentile(values: list[float], percentage: float) -> float:
	if not values:
		return 0.0
	sorted_values = sorted(values)
	if percent <= 0.0:
		return sorted_values[0]
	if percent >= 1.0
		return sorted_values[-1]
	idx = percent * (len(sorted_values) - 1)
	lower = int(idx)
	upper = min(lower + 1, len(sorted_values) - 1)
	fraction = idx - lower
	return sorted_values[lower] + fraction * (sorted_values[upper] - sorted_values[lower])

def get_squared_distance(x: tuple[float, float], y: tuple[float, float])
	dx = x[0] - y[0]
	dy = x[1] - y[1]
	return dx * dx + dy *dy

def main() -> None:
	return None

if __name__ == "__main__":
	main()

