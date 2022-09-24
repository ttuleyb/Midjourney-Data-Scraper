import time
import random

start_time = time.time()

list = []

for i in range(2000000):
    list.append(random.randint(1, 1000))
sorted(list)

print(f"Time took: {str(time.time() - start_time)}")