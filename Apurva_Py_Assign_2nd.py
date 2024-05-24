# (1) Python Code Execution Flow:

# Sequential Execution:     Python code executes line by line, from top to bottom.
                        
# Statements vs. Functions: Statements are simple actions (assignments, function calls, etc.),
#                           while functions are reusable blocks of code that can be called multiple times.

# Function Calls:
#                           When a function is called, execution jumps to the function's definition,
#                           executes its statements, and then returns to the line after the function call. 
#                           This creates a stack-like structure.

# Indentation Matters:      Indentation (usually spaces) defines code blocks within functions and control flow statements 
#                           (if, else, for, while). Inconsistent indentation can lead to errors.


# Example:

def greet(name):
    print(f"Hello, {name}! \n")

name = "Sir"
greet(name)  # Function call

# ==========================================================================================================================================


# (2)List Partition

# Divides a list into sublists based on a predicate function.
# Elements that evaluate to True in the predicate go into the first sublist, 
# and those that evaluate to False go into the second.

# Example: MANUAL LOOPING

def partition_by_word_length(words, max_short_length):
  """Partitions words by length"""
  short, long = [], []
  for word in words:
    if len(word) <= max_short_length:
      short.append(word)  # Short word
    else:
      long.append(word)  # Long word
  return short, long

words = ["apple", "banana", "watermelon", "orange", "pineapple"]
max_short_length = 6

short_words, long_words = partition_by_word_length(words, max_short_length)

print("Short words:", short_words)
print("Long words:", long_words)

# =====================================================================================================================================

# (3) Enum

# An enumeration (Enum) is a user-defined type that restricts values to a set of named constants. 
# It provides a safer and more readable way to represent fixed sets of values.

# Example:


from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    PURPLE = 3

favorite_color = Color.RED
print(f"\n My color is {favorite_color.name}.\n")  # Access name and value

# ========================================================================================================================================

# (4) Pass by Reference vs. Pass by Value

# Pass by Reference (Mutable Objects): When passing mutable objects (lists, dictionaries) to functions, 
#                                      changes made within the function affect the original object.
#                                      Python passes references to these objects.

# Pass by Value (Immutable Objects): When passing immutable objects (integers, strings, tuples) to functions,
#                                   a copy is passed, and changes within the function don't affect the original.

# Example:


def modify_list(my_list):  # Pass by reference (modifies original list)
    my_list.append(10)

def modify_string(my_string):  # Pass by value (copy created)
    my_string = "MY ASSIGNMENT"

my_list = [1, 2, 3]
modify_list(my_list)
print(my_list)  # Output: [1, 2, 3, 10]

my_string = "\nNITOR INFOTECH \n"
modify_string(my_string)
print(my_string)  # Output: Hello (original not modified)
# ===========================================================================================================================================


# (5) Union Operator with typing

# The Union type from the typing library allows specifying multiple possible types for a variable.

# Example:

from typing import Union

def handle_input(value: Union[int, str]):
    if isinstance(value, int):
        print(f"Integer: {value}")
    else:
        print(f"String: {value}")

handle_input(42)
handle_input("Apurva\n")
# ======================================================================================================================================

# (6) Checking if a Variable is Iterable

# 1. Using isinstance():

# This approach checks if the variable's type is a subclass of `collections.abc.Iterable`.
# This is the recommended method as it's clear and concise.

from collections.abc import Iterable

def is_iterable(obj):
  """Checks if an object is iterable using isinstance"""
  return isinstance(obj, Iterable)

my_list = [6.1, 2.9, 3.333,80]
my_string = "Slow but steady wins the race"

print(is_iterable(my_list))  # True
print(is_iterable(my_string))  # False


# 2. Using `try-except` block with iter():

# This method attempts to create an iterator from the variable using `iter()`. 
# If successful, the variable is iterable; otherwise, a `TypeError` is raised.


def is_iterable(obj):
  """Checks if an object is iterable using try-except"""
  try:
    iter(obj)
    return True
  except TypeError:
    return False

my_list = [1, 2, 3]
var_string = "RichieRich"
int_no = 8
Float_no = 3.14
Bool_val = True
None_type_var = None

print()
print(is_iterable(my_list)) 
print(is_iterable(int_no)) 
print(is_iterable(var_string))  
print(is_iterable(Float_no)) 
print(is_iterable(Bool_val)) 
print(is_iterable(None_type_var)) 

# =====================================================================================================================================
# (7) What are various ways to implement string formatting in python. 
# Answer:   
#         (1) F-strings :

#                            The most recent and convenient approach.
#                            They allow you to embed expressions directly within the string using curly braces {}.

name = "Sir"
no = 25

greeting = f"\nHello, {name}! This is {no}.\n"
print(greeting) 

# (2). format() method :


greeting_1 = "Hello, {}! This is {}.\n".format(name, no)  # Positional arguments
print(greeting_1) 


greeting_2 = "Hello, {name}! This is {no}.\n".format(name=name, no = no)  # Keyword arguments
print(greeting_2)  


# 3. % operator :

greeting_3 = "Hello, %s! This is %d. \n" % (name, no)
print(greeting_3)  

# ===================================================================================================================

# Give an example of any() and all().

numbers = [1, 0, 3, 0, 5]
strings = ["Big", "", "Data"]

# any() - Checks if at least one element is True (non-zero for numbers, non-empty for strings)

print("any(numbers):", any(numbers))  
print("any(strings):", any(strings))  

# all() - Checks if all elements are True (non-zero for numbers, non-empty for strings)

print("all(numbers):", all(numbers))  
print("all(strings):", all(strings))  

# ===================================================================================================================
# all functions fromITERTOOLS

from itertools import count, cycle, repeat, chain, compress, dropwhile, takewhile, groupby

# count: Infinite counter (start=10, step=2)
for num in count(10, 2):
  if num > 20:
    break
  print(num) 

# cycle: Repeats elements (colors list)
colors = ['red', 'green', 'blue']
color_cycle = cycle(colors)
print(next(color_cycle), next(color_cycle), next(color_cycle))  

# repeat: Repeat element ('X', 5 times)
repeated_char = repeat('X', 5)
print(''.join(repeated_char)) 

# chain: Concatenate iterables (numbers1 & numbers2)
numbers1 = [1, 2, 3]
numbers2 = [4, 5, 6]
combined_numbers = chain(numbers1, numbers2)
print(list(combined_numbers))  

# chain.from_iterable: Flatten nested iterables (nested_list)
nested_list = [[1, 2], [3, 4], [5]]
flattened_list = chain.from_iterable(nested_list)
print(list(flattened_list))  # [1, 2, 3, 4, 5]

# compress: Filter based on mask (numbers & even_mask)
numbers = [1, 4, 2, 8, 5]
even_mask = compress([True, False, True, False, True], numbers)
print(list(even_mask))  # [1, 2, 5] (even numbers)

# dropwhile: Skip elements (numbers with leading zero)
numbers = [0, 1, 3, 5, 7]
filtered_numbers = dropwhile(lambda x: x == 0, numbers)
print(list(filtered_numbers))  # [1, 3, 5, 7]

# takewhile: Get elements until condition fails (even numbers)
numbers = [2, 4, 6, 9, 10]
even_numbers = takewhile(lambda x: x % 2 == 0, numbers)
print(list(even_numbers)) 

# groupby: Group words by first letter
words = ["apple", "banana", "cherry", "apple", "orange"]
for letter, group in groupby(words, key=lambda x: x[0]):
  print(letter, list(group))

