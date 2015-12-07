#!/usr/bin/env python3
import gs2
import time
import random
import math
import jmath
import json
from jdebug import is_debug
import database
from collections import defaultdict

def get_vector(values, pos=10, size=10):
	return values[max(pos-size, 0):pos]

def splitDataset(dataset, splitRatio):
		trainSize = int(len(dataset) * splitRatio)
		trainSet = []
		copy = list(dataset)
		while len(trainSet) < trainSize:
				index = random.randrange(len(copy))
				trainSet.append(copy.pop(index))
		print('Split {0} files into train={1} and test={2} files...'.format(len(dataset), len(trainSet), len(copy)))
		return [trainSet, copy]

def get_classification(numbers, value):
	if value > jmath.get_peak_threshold(numbers):
		return "peak"
	return "nopeak"

def create_vocabulary(dataset):
	print("Creating vocabulary...")
	vocabulary_start_time = time.time()
	vocabulary = set()
	# Collect vocabulary

	for dset in dataset:
		for section in dset.get_values():
			for value in section:
				tmp_val = round(value, 2)
				vocabulary.add(tmp_val)

	print("Creating vocabulary took", time.time() - vocabulary_start_time,"seconds to create...")
	return vocabulary

def sort_by_class(dataset):
	print("Sorting by class")
	sort_by_class_start_time = time.time()
	mydict = lambda: defaultdict(mydict)
	sorted_values = {"peak":defaultdict(list), "nopeak":defaultdict(list)}

	for i,dset in enumerate(dataset):
		if i > 0 and is_debug:
			print("THIS IS DEBUGGING WE DONT NEED ALL THE VALUES")
			break

		sort_set_time = time.time()
		print("Set",i)

		for section in dset.get_values():
			for pos, value in enumerate(section):
				tmp_val = round(value, 2)
				try:
					grp = get_classification(section, tmp_val)
					# import pdb;pdb.set_trace()
					sorted_values[grp][tmp_val].append({'previous':get_vector(section, pos, 10)})
				except ZeroDivisionError:
					break

		print("Set",i,"took",time.time() - sort_set_time,"seconds to sort values for...")
	print("Sorting by class took", time.time() - sort_by_class_start_time,"seconds...")

	fname = 'sorted_all_data.json'

	if is_debug:
		fname ='sorted_all_data_debug.json'

	with open(fname, 'w') as fp:
		json.dump(sorted_values, fp)
	return sorted_values

def calculate_probability(x, mean, stdev):
	exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
	return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent

def calculate_group_probabilities(summaries, input_vector):
	probabilities = {}
	for classValue, classSummaries in summaries.items():
		probabilities[classValue] = 1
		for i in range(len(classSummaries)):
			mean, stdev = classSummaries[i]
			x = inputVector[i]
			probabilities[classValue] *= calculateProbability(x, mean, stdev)
	return probabilities

def predict(summaries, input_vector):
	probabilities = calculate_group_probabilities(summaries, input_vector)
	best_lab, best_prob = None, -1
	for group_value, probability in probabilities.items():
		if best_lab is None or probability > best_prob:
			best_prob = probability
			best_lab = group_value
	return best_lab

"""
def train(dataset):
	print("Training bayes...")
	train_start_time = time.time()
	mydict = lambda: defaultdict(mydict)
	p_val_given_class = mydict()
	vocabulary = create_vocabulary(dataset)

	for i, t in enumerate(dataset):
		if i > 0 and is_debug:
			print("THIS IS DEBUGGING WE DONT NEED ALL THE VALUES")
			break

		train_set_time = time.time()
		print("Set",i)

		section_values = t.get_values()
		num_sections = len(section_values)

		for j, section in enumerate(section_values):

			for k, value in enumerate(section):

				tmp_val = round(value, 2)
				classification = get_classification(section, tmp_val)
				p_val_given_class[classification][tmp_val] = p_val_given_class[classification].get(tmp_val, 0) + 1

		print("Set",i,"took",time.time() - train_set_time,"seconds to process...")

	print("Training took", time.time() - train_start_time,"seconds...")
	return p_val_given_class
"""




if __name__ == "__main__":
	pass
startTime = time.time()
all_files = gs2.load_json("all_data.json")
trainSet, testSet = splitDataset(all_files, 0.67)
s = sort_by_class(trainSet)


print("Bayes script took", time.time() - startTime, "seconds...")
