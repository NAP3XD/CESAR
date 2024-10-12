import requests
import threading

url = "https://192.168.1.211/production.json"
num_iterations = 100

success_count = 0
failure_count = 0
lock = threading.Lock()  # Lock for thread-safe incrementing

def download_file(url):
    global success_count, failure_count
    try:
        response = requests.get(url, timeout=10)  # Adjust timeout as needed
        if response.status_code == 200:
            with lock:
                success_count += 1
        else:
            with lock:
                failure_count += 1
    except Exception as e:
        with lock:
            failure_count += 1

# Create threads for concurrent downloads
threads = []
for i in range(num_iterations):
    t = threading.Thread(target=download_file, args=(url,))
    threads.append(t)
    t.start()

# Wait for all threads to complete (optional)
for t in threads:
    t.join()

# Calculate percentages
total_attempts = success_count + failure_count
success_percentage = (success_count / total_attempts) * 100 if total_attempts > 0 else 0
failure_percentage = (failure_count / total_attempts) * 100 if total_attempts > 0 else 0

# Print results
print(f"Total attempts: {total_attempts}")
print(f"Successful downloads: {success_count} ({success_percentage:.2f}%)")
print(f"Failed downloads: {failure_count} ({failure_percentage:.2f}%)")
