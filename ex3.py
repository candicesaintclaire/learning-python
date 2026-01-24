# Numbers and Math

# this line ouptuts the text "I will now count my chickens:" onto the screen
print("I will now count my chickens:")

#these two lines ouput  the words hens and/or Roosters, to the screen, with the corresponding number of each type.
#NOTE: that  order of operations matters here. so for hens, it's not 25 +30 then dividing that by 6 ... it's 30 div by 6, + 25. So we get 30.0 (note the "float int" or whatever it is called). 
print("Hens", 25 + 30 / 6)
#I am going to try to "break" this next line because the line above output with the  decimal space and i am curious to see how / vs % works re: decimal spaces etc. 
print("Roosters", 100 - 25 * 3 / 4)
#Okay so i changed it to a slash instead of a percentage sign and it does give us the decimals that way. next will add back the percent signs and confirm one last time. 

###### come back to this one!! print("last year I turned age. this year i am turning age+1)

print("Pink", 100 % 5)
print("Purple", 100 / 5)


print("Now I will count the eggs:")

print(3 + 2 + 1 - 5 + 4 % 2 - 1 / 4 + 6)

print("Is it true that 3 + 2 < 5 - 7?")

print(3 + 2 < 5 - 7)

print("What is 3 + 2?", 3 + 2)
print("What is 5 - 7?", 5 - 7)

print("Oh, that's why it's False.")

print("How about some more.")

print("Is it greater?", 5 > -2)
print("Is it greater or equal?", 5 >= -2)
print("Is it less or equal?", 5 <= -2)
