#!/usr/bin/env python3
import os
import time
import gs2

startTime = time.time()

FILE_LOCATION = "./GS2-filer/"  # Put gs2 files here
JSON_FILE = "all_data.json"
gs2s = []
try:
    gs2.load_json(JSON_FILE, gs2s)
except FileNotFoundError as ex:
    print(ex.strerror + ": ", ex.filename)
    if ex.filename == JSON_FILE:
        try:
            all_files = [f for f in os.listdir(FILE_LOCATION) if
                         os.path.isfile(os.path.join(FILE_LOCATION, f))]  # gets all files in folder

            files = [f for f in all_files if
                     f.lower().endswith(".gs2")]  # gets files that starts with uke
            for f in files:
                print("Processing", FILE_LOCATION + f + "...")
                data_object = gs2.GS2File()
                file = data_object.process_file(FILE_LOCATION + f)
                gs2s.append(data_object)
                print(FILE_LOCATION + f, "processed...")
            print("Saving to json:", JSON_FILE)
            gs2.save_json(gs2s, JSON_FILE)
            print("Saved to json file:", JSON_FILE)
        except FileNotFoundError as ex2:
            print(ex2.strerror + ": ", ex2.filename)

print("Script took", time.time() - startTime, "seconds...")
