#!/usr/bin/env python
import os
import time

import gs2

startTime = time.time()

FILE_LOCATION = "./GS2-filer/"

all_files = [f for f in os.listdir(FILE_LOCATION) if
             os.path.isfile(os.path.join(FILE_LOCATION, f))]  # gets all files in folder
files = [f for f in all_files if f.startswith("uke")]  # gets files that starts with uke

gs2s = []
for f in files:
    data_object = gs2.GS2File()
    data_object.process_file(FILE_LOCATION + f)
    gs2s.append(data_object)

gs2.load_json(gs2s, "uke_data.json")
# gs2.save_json(gs2s, "uke_data.json")

print("Script took", time.time() - startTime, "seconds...")
