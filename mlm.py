#!/usr/bin/env python3
from jdebug import is_debug
import database
import gs2
import jmath
import json
import random
import sqlite3
import sys
import time


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
                        cur.execute("insert into data ('value','vector','class') values (?,?,?)",[value, json.dumps(get_vector(section, pos, jmath.vector_length)), classification])
                    except ZeroDivisionError:
                        # Skip section if stddev is not possible
                        break
            sql_connection.commit()
            print("Sorting set",set_num,"took",time.time()-sort_data_set_time_start,"seconds...")

    sql_connection.close()
    print("Sorting all sets took",time.time()-sort_data_time_start,"seconds...")

def summarize_by_class():
    summarize_time_start = time.time()
    print("Summarizing...")
    con = sqlite3.connect(database.db_name)
    c = con.cursor()
    for group, groupval in get_class_values().items():
        print("Summarizing class",group)
        # Iterate over each of the attributes (components of the vector)
        for i in range(0,jmath.vector_length):
            print("Began processing vector index",i)

            # Iterate through many rows
            # by iterating through parts of the entire table
            row_limit = 100000 if is_debug else -1
            limit = 25000 if is_debug else 1000000
            offset = 0
            fetched_rows = 0

            # Where to store the temporary vector components
            atrib_i = []

            while fetched_rows < row_limit or row_limit == -1:
                iter_start_time = time.time()
                # Set the limit to limit or however many rows that are left if less than limit
                limit = limit if (limit+offset < row_limit or row_limit == -1) else (row_limit - fetched_rows)
                # Execute sql statement
                data = c.execute('select vector from data where class=? limit ? offset ?', [group, limit, offset]).fetchall()
                # How many rows returned
                data_len = len(data)
                offset += limit
                fetched_rows += data_len

                # Break out of loop if no more rows to process
                if data_len == 0:
                    break

                for row in data:
                    # Loads vectors into lists and forces their length
                    vec = json.loads(row[0])
                    vec = [-1.0]*(jmath.vector_length-len(vec))+vec
                    atrib_i.append(vec[i])

                print("Processed",str(fetched_rows)+", last",data_len,"processed in",time.time() - iter_start_time,"seconds...")
            #Calculate the summary
            try:
                atrib_sum = (jmath.mean(atrib_i), jmath.standard_deviation(atrib_i))
            except ZeroDivisionError as zde:
                import pdb;pdb.set_trace()

            print(atrib_sum)
    print("Summarizing took",time.time()-summarize_time_start,"seconds...")





start_time = time.time()
#dataset = gs2.load_json('all_data.json')
#train,test = split_dataset(dataset, 0.67)
if __name__ == '__main__':
    if 'resort' in sys.argv:
        sort_data(train)

    summarize_by_class()

print("Script finished in",time.time()-start_time,"seconds...")
