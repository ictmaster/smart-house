#!/usr/bin/env python3
import math


vector_length = 10

def mean(numbers):
	return sum(numbers)/float(len(numbers))

def standard_deviation(numbers):
	avg = mean(numbers)
	var = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(var)

def calculate_probability(x, mean, stdev):
	exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
	return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent


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
