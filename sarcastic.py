
import random

UPPERCASE_CHANCE = 0.3
def sarcastic(string): # Converts "Hello" to "hElLo"
	string = string.lower() # Convert to lowercase first.
	# 'tuple' object does not support item assignment
	out = []
	for c in string:
		out.append(c.upper()) if random.random() <= UPPERCASE_CHANCE else out.append(c)
	return "".join(out)

