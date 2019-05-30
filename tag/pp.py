import os

f = open("pronom.txt", "r")
d = ""
for x in f:
	x = x.capitalize()
	d += x;
		
with open("pronom.txt", 'w') as file:
	file.write(d)