## Q1
## Method 1
str1='Kavya'
a=(str1[0:5:2])
print(a)
b=list(a)
print(b)
b.reverse()
print(b)

## Method 2
str1="kavya"
str2=str1[-1::-2]
print(str2)

## Q2
str2='Mariyam'
x=str2.swapcase()
print(x)

## Q3 print current timestamp in python
import datetime
ct = datetime.datetime.now()
print("current time:-", ct)

# Q4 decorator vs generator
# Solution - Decorators allow us to wrap up another function in order to extend the behavior of another function. Whereas,
# a generator in Python is a special type of function that returns an iterator object. It appears similar 
# to a normal Python function in that its definition also starts with def keyword. However, instead of return 
# statement at the end, generator uses the yield keyword.

# Q5 walrus operator
# Solution- Walrus Operator allows you to assign a value to a variable within an expression. This can be useful when you need 
# to use a value multiple times in a loop, but don’t want to repeat the calculation.
# The Walrus Operator is represented by the := syntax and can be used in a variety of contexts including while loops and if statements. 

# Q6 function annotation
# Solution - Function annotations are arbitrary python expressions that are associated with various part of functions. 
# These expressions are evaluated at compile time and have no life in python’s runtime environment. 
# Python does not attach any meaning to these annotations. 
# They take life when interpreted by third party libraries, for example, mypy.

# Q7 format string vs raw string
# Soltuion - In Python, raw strings are defined by prefixing a string literal with the letter 'r'. 
# For example, a regular string would be defined as "Hello\nWorld", whereas a raw string would be defined as r"Hello\nWorld". 
# The 'r' prefix tells Python to treat the string as a raw string, meaning that escape sequences and special characters are 
# treated as literal characters rather than being interpreted.
# The format() method is a powerful tool that allows developers to create formatted strings by embedding variables and
#  values into placeholders within a template string. 

# Q8 / and // difference
# Solution- / division and // floor division

# Q9 reindexing in pandas
# Solution - Reindexing is used to change the row labels and column labels of a DataFrame. It means to 
# confirm the data to match a given set of labels along a particular axis.

# Q10 create a dictionary and fill empty spaces with default values
my_dict = {'a': 1, 'b': '', 'c': 3, 'd': ''}
default_value = 0
for key in my_dict:
    if my_dict[key] == '':
        my_dict[key] = default_value
print(my_dict)

# Q11 rolling mean
# Solution- Pandas dataframe.rolling() function provides the feature of 
# rolling window calculations. The concept of rolling window calculation is most primarily used in signal processing and time-series data.

# Q12 pickling
# Solution - Pickle in Python is primarily used in serializing and deserializing a Python object structure. In other words, it's the process of converting
#  a Python object into a byte stream to store it in a file/database, maintain program state across sessions, or transport data over the network.

# Q13 create a dataframe in pandas and find sum of a columns
#Soltuion 
import pandas as pd
data = {'A': [1, 2, 3, 4, 5],
        'B': [6, 7, 8, 9, 10],
        'C': [11, 12, 13, 14, 15]}

df = pd.DataFrame(data)
print("DataFrame:")
print(df)
column_name = 'B'
column_sum = df[column_name].sum()
print(f"\nSum of column '{column_name}': {column_sum}")

# Q14 can we do tuple comprehension
# Tuple comprehension is not possible becauseco mprehension grows the structure, which means adding one item at a time and tuples 
# are fixed.

# Q15 sort and sorted
# Solution- The primary difference between sort() and sorted() is the return value. 
# sort() returns None because it modifies the original list in-place. sorted(), on the other hand, returns a new sorted list.

# Q16 concat vs append
# Solution- The concat method can combine data frames along either rows or columns, while the append method only combines data frames 
# along rows. Another important difference is that concat can combine more than two data frames at once, while append only 
# appends one data frame to another.

# Q17 best way to create a dictionary according to linters
# Solution - Consistent Indentation,Descriptive Variable Names,Single Quotes for Keys and Values,Vertical Alignment,Trailing Comma
# Example 1 - Basic dictionary creation
# my_dict = {'key1': 'value1','key2': 'value2'}
# Example 2 - Dictionary with descriptive variable names
# user_info = {'name': 'John Doe','age': 30,'email': 'john@example.com'}
# Example 3 - Using vertical alignment
# employee_info = {
#     'name':     'Alice',
#     'age':      35,
#     'position': 'Manager',
#     'salary':   75000,
# }
# Example 4- Dictionary with trailing comma
# options = {
#     'debug': False,
#     'verbose': True,
#     'mode': 'fast',
# }

# Q18 D=dict(); for x in enumerate(range(2)): D[x[0]]=x[1] D[x[1]+7]=x[0]
# Solution - {0:0,7:0,1:1,8:1}

# Q19 Timedelta
# Solution - Python timedelta() function is present under datetime library which is generally used for 
# calculating differences in dates and also can be used for date manipulations in Python. 
# It is one of the easiest ways to perform date manipulations. 

#Q20  Multi-index 
# Solution -  Multi-index allows you to represent data with multi-levels of indexing, creating a hierarchy in rows and columns.

#Q21 Head() and tail()
#Solution- head returns the top 5 values by default of a dataframe and tail returns the bottom 5 values of a dataframe

#Q22 Sort by and group by pandas
# Solution - By using DataFrame. sort_values() , you can sort DataFrame in ascending or descending order, before going to sort the grouped data,
# we need to group the DataFrame rows by using DataFrame. groupby() method. Note that groupby preserves the order of rows within each group.

#Q23 Ways to optimize pandas
# Solution- Vectorized Operations: Pandas is designed to perform well with vectorized operations, so try to avoid using iterative operations like loops.
# Correct Data Types: Choose appropriate data types for your columns to reduce memory usage and improve performance. 
# Categorical Data: If a column has a limited number of unique values, consider converting it to a categorical data type using pd.Categorical(). 
# Memory Efficient Methods: Use memory-efficient methods like read_csv() with appropriate parameters (dtype, usecols, chunksize) 
# to reduce memory usage when reading large datasets.
# Avoid Chained Indexing: Chained indexing (e.g., df['column'][index]) can create copies of data and lead to performance issues. Instead, use .loc[] or .iloc[].
# Optimize Groupby Operations: Groupby operations can be memory-intensive. Try to minimize the number of groups and use agg() with a dictionary

# Q24 How to empty a dictionary
# Solution- Use clear.
