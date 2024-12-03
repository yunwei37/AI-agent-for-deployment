import ray

# Initialize Ray
ray.init()

# Define a remote function
@ray.remote
def say_hello():
    return "Hello, World!"

# Execute the remote function and get the result
result = ray.get(say_hello.remote())

# Print the result
print(result)

# Shut down Ray
ray.shutdown()
