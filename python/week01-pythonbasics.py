"""
Basic code from week 01. Notably, this is a 'comment' (that is, it is used to explain code, and
will not be executed when the code is run). 

@auth dpb
@date 10/01/2013

Comments in python are denoted either by the hash symbol (this works at any point on the line in 
which it appears, for one line. See below), or by the triple-quote surrounded text you see here
(which obviously work across lines).

Now you have no excuse: comment your code. Love Duncan.

Also, notice that all the lines in this file are, at most, 100 characters long. This is a point of
style, which we will also be talking about (for those oldschoolers among us, 100 is the new 
standard. It used to be 80).
"""

# Basic commands. Note that you can copy and paste these lines into the interactive Python terminal
str_variable = "Testing strings for fun"
int_variable = 1234
dec_variable = 12.34
another_variable = "This is another string, but it could be anything"

# Print these variables. Use the string 'format' method, as shown. It's easier and better
print "String: {0}, integer: {1}, decimal: {2}".format(str_variable, int_variable, dec_variable)

# Here is statement that will not work (can not add a string to a number)
# Because it will cause this script to fail, you can "comment it out" (put a '#' at the beginning
# of the line).
print "String plus int: {0}".format(int_variable + str_variable)

# Here is an addition statement that will work. Python is able to add integers to decimals, because
# they are both numbers. The result will be  a decimal
print "Decimal plus int: {0}".format( dec_variable + int_variable)


# Basic lists and functions
word_list = ["government", "shutdown", "crazy?"]

print "Words of interest: {0}".format(word_list)
print "Number of words of interest: {0}".format(len(word_list))

# Useful list functions. Use 'map' to apply a function to all elements of a list
words_length = map(len, word_list)
print "The length of each word in list (in order): {0}".format(words_length)

# Use a string function to join all elements of a list together
words_str = "|".join(word_list)
print "Joined words: {0}".format(words_str)