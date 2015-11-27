#!/usr/bin/env python3
import gs2
import time
import random
import math

def get_vector(values, pos=10, size=10):
	return values[pos:pos+size]
	
def splitDataset(dataset, splitRatio):
		trainSize = int(len(dataset) * splitRatio)
		trainSet = []
		copy = list(dataset)
		while len(trainSet) < trainSize:
				index = random.randrange(len(copy))
				trainSet.append(copy.pop(index))
		return [trainSet, copy]

def separateByClass(dataset):
	separated = dict()
	for i in range(len(dataset)):
		vector = dataset[i].get_values()
		# TODO


if __name__ == "__main__":
	startTime = time.time()
	JSON_FILE = "all_data.json"
	print("Loading json...")
	dataset = gs2.load_json(JSON_FILE)
	print("Loaded " + JSON_FILE + "...")
	print("Training bayes...")

	trainingSet, testSet = splitDataset(dataset, 0.67)
	print('Split {0} files into train={1} and test={2} files...'.format(len(dataset), len(trainingSet), len(testSet)))



	print("Bayes scripit took", time.time() - startTime, "seconds...")
