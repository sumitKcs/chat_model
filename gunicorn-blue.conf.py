import multiprocessing

# Set the bind address and port
bind = "127.0.0.1:6636"

# Set the number of workers
# workers = multiprocessing.cpu_count() * 2 + 1  # 33 workers for a 16-core CPU
workers = 4

# Use Uvicorn workers for asynchronous support
worker_class = "uvicorn.workers.UvicornWorker"

# Enable threads
threads = 4  # Start with 16 threads and adjust based on performance
