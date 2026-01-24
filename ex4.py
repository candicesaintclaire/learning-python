# Variables and Names

# Write a comment above each line explaining to yourself what it does, in English
# Read your .py file backward
# Read your .py file out loud, saying even the characters

#this defines the variable cars to be an integer equal to 100
cars = 100

#this defines the variable space_in_a_car to be a floating point  of 4.0
space_in_a_car= 4.0

#this defines the variable drivers to be an int of 30
drivers = 30

#this defines the variable passengers to be an int of 90
passengers = 90

#this defines the variable cars_not_driven as  the difference between the variables cars and drivers
cars_not_driven = cars - drivers
cars_driven = drivers
carpool_capacity = cars_driven * space_in_a_car
average_passengers_per_car = passengers / cars_driven

print("There are", cars, "cars available.")
print("There are only", drivers, "drivers available.")
print("There will be", cars_not_driven, "empty cars today.")
print("We can transport", carpool_capacity, "people today.")
print("We have", passengers, "to carpool today.")
print("We need to put about", average_passengers_per_car, "in each car.")

# Study Drills

# Explain the error in Zed's code

# In the ex4.py code he provides, "car_pool_capacity" is not defined; it's written as "carpool_capacity" instead. This is why there was an error. It occurred on  Line 7 in his provied code. 

