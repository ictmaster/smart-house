#!/usr/bin/env python3
import gs2
import time

startTime = time.time()
JSON_FILE = "all_data.json"

files = gs2.load_json(JSON_FILE)

print("Bayes script took", time.time() - startTime, "seconds...")
