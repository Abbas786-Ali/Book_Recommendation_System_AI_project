## ALI ABBAS 
import time
start_time = time.time()

with open('c:/Users/abc\Desktop/storage.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        product_id, name, price = line.strip().split(',')
        if product_id == '101':
            print(f"Data from Storage: {name} - {price}")
            break

end_time = time.time()

print(f"Time taken to read from storage: {end_time - start_time} seconds")