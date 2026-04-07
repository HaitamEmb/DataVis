#Functions that calculate the mean, median, min, max, first, second and third quartiles

import math

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
