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
import os

def get_class_values():
    return {'nopeak':0, 'peak':1}

def get_classification(numbers, value):
	if value > jmath.get_peak_threshold(numbers):
		return "peak"
	return "nopeak"

def get_vector(numbers, pos, size=10):
    return numbers[max(pos-size,0):pos]

def get_vector_f(numbers, pos, size=jmath.vector_length):
    vec = numbers[max(pos-size,0):pos]
    vec = [-1.0]*(jmath.vector_length-len(vec))+vec
    return vec

def split_dataset(dataset, split_ratio):
    print("Splitting dataset...")
    train_size  = int(len(dataset) * split_ratio)
    train_set   = []
    test_set    = []
    ratio_fname = 'test_train_ratio.json'
    if os.path.isfile(ratio_fname):
        print("There seems to be a ratio file already, sorting like file if names are equal...")
        names_with_index = {dset.name:i for i, dset in enumerate(dataset)}
        with open(ratio_fname, 'r') as ttr:
            d = json.load(ttr)
            # Check if files are the same
            if set(names_with_index.keys()) == set([item for sublist in d.values() for item in sublist]):
                for name, index in names_with_index.items():
                    if name in d['training']:
                        train_set.append(dataset[index])
                    else:
                        test_set.append(dataset[index])
            else:
                print("Files doesn't match, quitting...")
                sys.exit(1)
        return [train_set, test_set]

    test_set = list(dataset)
    while len(train_set) < train_size:
        index = random.randrange(len(test_set))
        train_set.append(test_set.pop(index))
    # Save file for remembering which files are used for testing
    with open(ratio_fname, 'w') as ttr:
        d = {'training':[x.name for x in train_set],
        'testing':[x.name for x in test_set]}
        json.dump(d, ttr)
    return [train_set, test_set]

def sort_data(dataset):
    print("Sorting data into database...")

    sort_data_time_start = time.time()

    sql_connection = sqlite3.connect(database.db_name)
    cur = sql_connection.cursor()

    # Lets not fuck up sorted data by creating duplicate data
    if cur.execute('select count(*) from data;').fetchall()[0][0] != 0:
        print("There is already rows in the table...")
        return

    for set_num, data in enumerate(dataset):
            print("Sorting set",set_num)
            sort_data_set_time_start = time.time()

            for section_number, section in enumerate(data.get_values()):
                try:
                    threshold = jmath.get_peak_threshold(section)
                except ZeroDivisionError:
                    # Skip section if stddev is not possible
                    break
                for pos, value in enumerate(section):
                    classification = 'peak' if value > threshold else 'nopeak'
                    cur.execute("insert into data ('value','vector','class') values (?,?,?)",[value, json.dumps(get_vector(section, pos, jmath.vector_length)), classification])
            sql_connection.commit()
            print("Sorting set",set_num,"took",time.time()-sort_data_set_time_start,"seconds...")

    sql_connection.close()
    print("Sorting all sets took",time.time()-sort_data_time_start,"seconds...")

def summarize_by_class():
    summarize_time_start = time.time()
    print("Summarizing...")
    con = sqlite3.connect(database.db_name)
    c   = con.cursor()

    # Lets not fuck up summaries by creating duplicate data
    if c.execute('select count(*) from summaries;').fetchall()[0][0] != 0:
        print("There is already rows in the table...")
        return

    for group, groupval in get_class_values().items():
        print("Summarizing class",group)
        # Iterate over each of the attributes (components of the vector)
        for i in range(0,jmath.vector_length):
            print("Began processing vector index",i,"in class",group)

            # Iterate through many rows
            # by iterating through parts of the entire table
            row_limit    = 100000 if is_debug else -1
            limit        = 25000 if is_debug else 1000000
            offset       = 0
            fetched_rows = 0
            # Where to store the temporary vector components
            atrib_i      = []


            while fetched_rows < row_limit or row_limit == -1:
                iter_start_time = time.time()
                # Set the limit to limit or num of rows that are left
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
            # Calculate the summary
            try:
                atrib_sum = [jmath.mean(atrib_i), jmath.standard_deviation(atrib_i)]
            except ZeroDivisionError as zde:
                import pdb;pdb.set_trace()
            print(atrib_sum)
            c.execute('insert into summaries (summary, vector_index, class) values (?, ?, ?);',[json.dumps(atrib_sum), i, group])
            con.commit()
    con.close()
    print("Summarizing took",time.time()-summarize_time_start,"seconds...")

def calculate_class_probabilities(summaries, input_vector):
        probabilities = {}
        for classValue, classSummaries in summaries.items():
                probabilities[classValue] = 1
                for i in range(len(classSummaries)):
                        mean, stdev = classSummaries[i]
                        x = input_vector[i]
                        probabilities[classValue] *= jmath.calculate_probability(x, mean, stdev)
        return probabilities

def predict(summaries, input_vector):
        probabilities = calculate_class_probabilities(summaries, input_vector)
        bestLabel, bestProb = None, -1
        for classValue, probability in probabilities.items():
                if bestLabel is None or probability > bestProb:
                        bestProb = probability
                        bestLabel = classValue
        return bestLabel

def print_accuracy(total, predicted, true_pred, false_pred):
    print("""
        Predicted: {0} out of {1} correct! ({2}%)
        Predicted: {3} out of {4} peaks correct! ({5}%)
        Predicted: {6} out of {7} nopeaks correct! ({8}%)
        Total accuracy: {9}%""".format(
        sum(true_pred.values()), sum(total.values()), 100*(sum(true_pred.values())/float(sum(total.values()))),
        true_pred['peak'], total['peak'], 100*(true_pred['peak']/float(total['peak'])),
        true_pred['nopeak'], total['nopeak'], 100*(true_pred['nopeak']/float(total['nopeak'])),
        100*(sum(true_pred.values())/float(sum(total.values())))
        ))

if __name__ == '__main__':
    start_time = time.time()
    dataset    = gs2.load_json('all_data.json')
    train,test = split_dataset(dataset, 0.67)
    # TODO: Resort and resummarize so we know which files are training and which files are testing
    if 'resort' in sys.argv:
        sort_data(train)
    if 'resummarize' in sys.argv:
        summarize_by_class()

    summaries = database.get_summaries()
    if 'test' in sys.argv:
        t_predictions = {'total':{'peak':0, 'nopeak':0},'predicted':{'peak':0, 'nopeak':0},'true_pred':{'peak':0, 'nopeak':0},'false_pred':{'peak':0, 'nopeak':0}}
        for ts in test:
            print("Testing "+ts.name+"...")
            f_predictions = {'total':{'peak':0, 'nopeak':0},'predicted':{'peak':0, 'nopeak':0},'true_pred':{'peak':0, 'nopeak':0},'false_pred':{'peak':0, 'nopeak':0}}
            file_time_start = time.time()
            for s in ts.sections:
                try:
                    x = s.get_values()
                    for pos,val in enumerate(x):
                        prediction = predict(summaries, get_vector_f(x,pos))
                        realval = get_classification(x,val)

                        f_predictions['predicted'][prediction] += 1
                        f_predictions['total'][realval] += 1
                        t_predictions['predicted'][prediction] += 1
                        t_predictions['total'][realval] += 1
                        if prediction == realval:
                            f_predictions['true_pred'][prediction] += 1
                            t_predictions['true_pred'][prediction] += 1
                        else:
                            f_predictions['false_pred'][prediction] += 1
                            t_predictions['false_pred'][prediction] += 1
                except TypeError:
                    continue
            print_accuracy(f_predictions['total'], f_predictions['predicted'], f_predictions['true_pred'], f_predictions['false_pred'])
            print("\n\t"+ts.name+" tested in "+str(time.time() - file_time_start)+" seconds...\n\n")
        print("Total:")
        print("\t" + str(t_predictions))
        print_accuracy(t_predictions['total'], t_predictions['predicted'], t_predictions['true_pred'], t_predictions['false_pred'])
        print("\n")


print("Script finished in",time.time()-start_time,"seconds...")
