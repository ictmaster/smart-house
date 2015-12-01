#!/usr/bin/env python3
import math

def mean(numbers):
	return sum(numbers)/float(len(numbers))

def standard_deviation(numbers):
	avg = mean(numbers)
	var = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(var)

def is_float(val):
    try: 
        float(val)
        return True
    except ValueError:
        return False

def get_peak_threshold(numbers):
    return mean(numbers) + standard_deviation(numbers)

def is_peak(numbers, value_position):
    if numbers[value_position] > get_peak_threshold(numbers):
        return True
    else:
        return False

def has_peak(numbers):
	peak_threshold = get_peak_threshold(numbers)
	for num in numbers:
		if num > peak_threshold:
			return True
	return False