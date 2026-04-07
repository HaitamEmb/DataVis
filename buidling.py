from __future__ import annotations
import matplotlib.pyplot as plt
import sys
import psycopg2
import os
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