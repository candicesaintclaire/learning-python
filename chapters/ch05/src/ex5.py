# LEARN PYTHON 3 THE HARD WAY - ZED SHAW

# EXERCISE 5: VARIABLES AND NAMES

# WHAT I HAVE LEARNED SO FAR: Printing statements to the screen/terminal via the "print" statement; using math operators to do math. 

# Notes: 

# This section is about variables. A variable is a name for something, kind of like how "Zed" is a variable for "the human who wrote the book I am reading & learning Python 3 with". 

# Task:  as usual, type out, by hand, all of the code in the book; additionally: (1) write a comment above each line that explains what that line is doing, in plain English, (2) read the .py file backwards, and (3) read the .py file out loud, saying the words & characters

cars = 100
space_in_car = 4
drivers = 30 
passengers = 90
cars_not_driven = cars - drivers
cars_driven = drivers
carpool_capacity = cars_driven * space_in_car
average_passengers_per_car = passengers / cars_driven

print("There are", cars, "cars available.")
print("There are only", drivers, "drivers available.")
print("There will be", cars_not_driven, "empty cars today.")
print("We can transport", carpool_capacity, "people today.")
print("We have", passengers, "to carpool today.")
print("We need to put about", average_passengers_per_car, "in each car.")

# #####################

# STUDY DRILLS 

# 0) Zed's mistake when he first wrote the program: he used the variable "car_pool_capacity" at line 8, however, "car_pool_capacity" is not defined; it's "carpool_capacity" with only 1 underscore. Therefore, it threw an error with the name of the variable which again, was because that variable had not been defined so Python doesn't know what to put in place of "car_pool_capacity".

# 1) if you use "4" instead of "4.0" when defining the variable space_in_a_car, you get the same output, therefore, in this instance, it is not necessary to use the ".0" and make 4.0 a floating point variable. 

# 2) 
