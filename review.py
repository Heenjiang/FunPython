# Review 1

def add_to_list(value, my_list=[]):
    my_list.append(value)

    return my_list
"""
Issue: When using mutable default arguments, the list is shared across all function calls

Fix:

def add_to_list(value, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(value)
    return my_list
"""

# Review 2

def format_greeting(name, age):
    return "Hello, my name is {name} and I am {age} years old."

"""
Issue: The f-string or str.format() is missing to properly substitute variables.

Fix:

# Using f-string
def format_greeting(name, age):
    return f"Hello, my name is {name} and I am {age} years old."

# Alternatively, using .format()
def format_greeting(name, age):
    return "Hello, my name is {} and I am {} years old.".format(name, age)
"""

# Review 3

class Counter:
    count = 0

    def __init__(self):
        self.count += 1

    def get_count(self):
        return self.count

"""
Issue: The count variable is defined as a class attribute, meaning it is shared among all instances of the class. 
However, in the __init__ method, self.count is used, which creates an instance instead. 


class Counter:
    def __init__(self):
        self.count = 1

    def get_count(self):
        return self.count

"""

# Review 4

import threading


class SafeCounter:

    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1


def worker(counter):
    for _ in range(1000):
        counter.increment()


counter = SafeCounter()

threads = []

for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))

    t.start()

    threads.append(t)

for t in threads:
    t.join()

"""
Issue: The increment method is not thread-safe.

Fix:
Use a threading lock to synchronize access to self.count.

import threading

class SafeCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1

def worker(counter):
    for _ in range(1000):
        counter.increment()

counter = SafeCounter()
threads = []
for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
"""

# Review 5

def count_occurrences(lst):
    counts = {}

    for item in lst:

        if item in counts:

            counts[item] = + 1

        else:

            counts[item] = 1

    return counts

"""

Fix:
Change =+ 1 to += 1.

def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts
"""

