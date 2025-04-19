def add(x, y):
    print(f"x={x}, y={y}")  # Debugging print
    return x + y

result = add(3, 5)
print("Result:", result)


# import pdb

# def divide(x, y):
#     pdb.set_trace()  # Debugger stops here
#     return x / y

# print(divide(10, 2))



import logging

# Basic config: level & message format
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

# Example usage
logging.debug("This is a debug message")    # Detailed info (used for debugging)
logging.info("This is an info message")     # General info
logging.warning("This is a warning")        # Warning
logging.error("This is an error")           # Error message
logging.critical("This is critical")        # Severe error

print("\n")


def divide(a, b):
    logging.debug(f"Trying to divide {a} by {b}")
    if b == 0:
        logging.error("Division by zero!")
        return None
    return a / b

result = divide(10, 0)


import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

logging.info("This message goes to the log file.")
