# This is a large test file for evaluating tokenization and Prometheus metrics

# Some simple arithmetic operations
a = 10 + 25 - 3 * 2 / 4
b = 7 * (8 - 4)

# Variable assignments with different types of literals
x = 42  # Integer
y = 3.14  # Float
z = "Hello, World!"  # String
is_valid = True  # Boolean

# If-else conditionals
if x > 10:
    print("x is greater than 10")
else:
    print("x is not greater than 10")

# While loop
i = 0
while i < 5:
    print(f"i = {i}")
    i += 1

# For loop iterating over a range
for i in range(10):
    if i % 2 == 0:
        print(f"Even number: {i}")
    else:
        print(f"Odd number: {i}")

# Function definition with parameters and return value
def calculate_area(radius):
    pi = 3.14159
    return pi * radius * radius

# Function calls
result = calculate_area(5)
print(f"Area: {result}")

# Some complex expressions
expression_1 = (x + y) * (z == "Hello, World!") - 10
expression_2 = (b * 2) / 3 + a

# Define a class with methods
class ExampleClass:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, {self.name}!")

# Create an instance of ExampleClass
obj = ExampleClass("John")
obj.greet()

# List of numbers with conditional expression inside a list comprehension
numbers = [i for i in range(100) if i % 2 == 0]

# String manipulation: concatenation, slicing, etc.
s = "Prometheus"
s += " Monitoring"
substring = s[0:9]

# Array (list) manipulation
arr = [1, 2, 3]
arr.append(4)
arr.insert(0, 0)

# Dictionary (hash map) operations
person = {"name": "Alice", "age": 30, "city": "Wonderland"}
person["city"] = "New York"
person["profession"] = "Engineer"

# Set operations
my_set = {1, 2, 3, 4, 5}
my_set.add(6)
my_set.remove(1)

# Comments (should be ignored by tokenizer)
# This is a single-line comment

"""
This is a multi-line
comment that spans
across multiple lines.
"""

# Edge case with unbalanced parentheses, braces, and brackets
unbalanced_expression = "{[()]}("
unbalanced_expression2 = "({[})]"

# Error scenario
error_scenario = "this is an invalid token !!"

# Large numerical calculations
large_num = 1e10  # 10^10
small_num = 1e-10  # 10^-10

# Mixed expressions
complex_expr = (a + b * (x / y)) - (z == "Hello")

# Call a function with a complex argument
print(calculate_area(large_num))

# Complex boolean expressions
if (a == b or y < z) and (x > 10):
    print("Complex condition passed")



# Some more advanced expressions
matrix = [[1, 2], [3, 4]]
matrix_transpose = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

# Final test for tokenization
final_expression = "x + y * (z == 'Hello') / 3.14 - 5"
