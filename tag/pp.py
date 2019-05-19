import os

f = open("organisation.txt", "r")
d = ""
for x in f:
	x = x.capitalize()
	d += x;
		
with open("organisation_maj.txt", 'w') as file:
	file.write(d)