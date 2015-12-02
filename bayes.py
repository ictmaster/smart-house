#!/usr/bin/env python3
import gs2
import time
import random
import math
import jmath
import json
from jdebug import is_debug
from collections import defaultdict

def get_vector(values, pos=10, size=10):
	return values[pos:pos+size]
	
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
		return True
	return False

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
	sorted_values = {True:set(), False:set()}

	for i,dset in enumerate(dataset):
		if i > 0 and is_debug:
			print("THIS IS DEBUGGING WE DONT NEED ALL THE VALUES")
			break

		sort_set_time = time.time()
		print("Set",i)

		for section in dset.get_values():
			for value in section:
				tmp_val = round(value, 2)
				sorted_values[get_classification(section, tmp_val)].add(tmp_val)

		print("Set",i,"took",time.time() - sort_set_time,"seconds to sort values for...")
	print("Sorting by class took", time.time() - sort_by_class_start_time,"seconds...")
	with open('sorted_all_data.json', 'w') as fp:
		json.dump(sorted_values, fp)
	return sorted_values


def train(dataset):
	print("Training bayes...")
	train_start_time = time.time()
	mydict = lambda: defaultdict(mydict)
	p_val_given_class = mydict()
	# vocabulary = create_vocabulary(dataset)

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





if __name__ == "__main__":
	pass
startTime = time.time()
JSON_FILE = "all_data.json"
print("Loading json...")
dataset = gs2.load_json(JSON_FILE)
print("Loaded " + JSON_FILE + "...")
trainingSet, testSet = splitDataset(dataset, 0.67)
s = create_vocabulary(trainingSet)
# values = train(trainingSet)



print("timestamp:",time.time() - startTime, "seconds...")
print("Bayes script took", time.time() - startTime, "seconds...")
