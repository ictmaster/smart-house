#!/usr/bin/env python3
import gs2
import time
import json
import jmath
from jdebug import is_debug
import random
import database
import sqlite3

def get_class_values():
    return {'nopeak':0, 'peak':1}

def get_classification(numbers, value):
	if value > jmath.get_peak_threshold(numbers):
		return "peak"
	return "nopeak"

def get_vector(numbers, pos, size=10):
    return numbers[max(pos-size,0):pos]

def split_dataset(dataset, split_ratio):
    trainSize = int(len(dataset) * split_ratio)
    trainSet = []
    copy = list(dataset)
    while len(trainSet) < trainSize:
        index = random.randrange(len(copy))
        trainSet.append(copy.pop(index))
    return [trainSet, copy]

def sort_data(dataset):
    print("Sorting data into database...")

    sort_data_time_start = time.time()

    sql_connection = sqlite3.connect(database.db_name)
    cur = sql_connection.cursor()

    for set_num, data in enumerate(dataset):
            print("Sorting set",set_num)
            sort_data_set_time_start = time.time()

            for section_number, section in enumerate(data.get_values()):
                threshold = jmath.get_peak_threshold(section)
                for pos, value in enumerate(section):
                    try:
                        classification = 'peak' if value > threshold else 'nopeak'
                        cur.execute("insert into data ('value','vector','class') values (?,?,?)",[value, json.dumps(get_vector(section, pos)), classification])
                    except ZeroDivisionError:
                        # Skip section if stddev is not possible
                        break
            sql_connection.commit()
            print("Sorting set",set_num,"took",time.time()-sort_data_set_time_start,"seconds...")

    sql_connection.close()
    print("Sorting all sets took",time.time()-sort_data_time_start,"seconds...")

start_time = time.time()
dataset = gs2.load_json('all_data.json')
train,test = split_dataset(dataset, 0.67)

sort_data(train)


print("Script finished in",time.time()-start_time,"seconds...")
