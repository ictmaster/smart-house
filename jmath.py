#!/usr/bin/env python3
import math

def mean(numbers):
	return sum(numbers)/float(len(numbers))

def standard_deviation(numbers):
	avg = mean(numbers)
	var = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(var)

