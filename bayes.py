#!/usr/bin/env python3
import gs2
import time
import random
import math
import jmath

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
	pass
startTime = time.time()
JSON_FILE = "all_data.json"
print("Loading json...")
dataset = gs2.load_json(JSON_FILE)
print("Loaded " + JSON_FILE + "...")
print("timestamp:",time.time() - startTime, "seconds...")
print("Training bayes...")
trainingSet, testSet = splitDataset(dataset, 0.67)

num_of_class = dict()
for i, t in enumerate(trainingSet):
	if i != 0:
		break
	print("Set",i)
	num_sections = len(t.get_values())
	for j, section in enumerate(t.get_values()):
		print("Section",j,"out of",num_sections)
		for k, value in enumerate(section):
			is_peak = jmath.is_peak(section, k)
			num_of_class[is_peak] = num_of_class.get(is_peak, 0) + 1

print(num_of_class)


print("timestamp:",time.time() - startTime, "seconds...")
print('Split {0} files into train={1} and test={2} files...'.format(len(dataset), len(trainingSet), len(testSet)))
print("Bayes script took", time.time() - startTime, "seconds...")
