#!/usr/bin/env python3
import gs2
import time


def train_bayes(training_file):
    groups = {}
    training_data = []
    # Only use if section is Time-series
    for section in training_file.sections:
        if section.name == "Time-series":
            pass  # Either calculate deviation for one house or store all values somewhere


if __name__ == "__main__":
    startTime = time.time()
    JSON_FILE = "all_data.json"
    print("Loading json...")
    files = gs2.load_json(JSON_FILE)
    print("Loaded " + JSON_FILE + "...")
    print("Training bayes...")
    train_bayes(files[0])

    print("Bayes script took", time.time() - startTime, "seconds...")
