import time
from pathlib import Path
import os
from datetime import datetime
paths = Path("jsons").glob("*.json")

today = datetime.today().strftime('%Y-%m-%d')

start_time = time.time()

import lexica_farmer_run_daily

print(f"60 Threads: {str(time.time() - start_time)}")
first_result = str(time.time() - start_time)

#Move all files to a folder with date as its name
if not os.path.exists("jsons\\" + today):
    os.makedirs("jsons\\" + today)

for i in paths:
    filePath = "jsons\\" + i.name
    os.rename(filePath, "jsons\\" + today + "\\" + i.name)
    print(filePath)

start_time = time.time()

import lexica_farmer_run_daily_limited

print(f"12 Threads: {str(time.time() - start_time)}")
print(f"60 Threads: {first_result}")