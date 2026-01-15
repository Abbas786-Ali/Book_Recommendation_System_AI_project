## ALI ABBAS
import time

# Cache stored in memory
cache = {
    101: "Laptop - 120000",
    102: "Mobile - 80000",
    103: "Headphones - 15000",
    104: "Keyboard - 7000",
    105: "Mouse - 3500"
}

start_time = time.time()
data = cache[101]
end_time = time.time()

print("Data from Cache:")
print(data)
print(f"Time taken to read from cache: {end_time - start_time} seconds")