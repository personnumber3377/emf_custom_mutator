
import random


def mutate_integer(value: int, n: int) -> int: # Thanks ChatGPT!!!
	"""Randomly mutates an integer while ensuring it fits within n bytes.

	Args:
		value (int): The integer to mutate.
		n (int): The maximum number of bytes.

	Returns:
		int: The mutated integer.
	"""
	if n <= 0:
		raise ValueError("Number of bytes (n) must be positive.")
	
	# Maximum value that fits in n bytes
	max_value = (1 << (n * 8)) - 1

	# Choose a random mutation
	mutation = random.choice(["left_shift", "right_shift", "bit_flip", "add", "subtract"])

	if mutation == "left_shift":
		shift = random.randint(1, n * 8 - 1)  # Shift amount
		value = (value << shift) & max_value  # Ensure it fits in n bytes

	elif mutation == "right_shift":
		shift = random.randint(1, n * 8 - 1)  # Shift amount
		value = value >> shift

	elif mutation == "bit_flip":
		bit_to_flip = random.randint(0, n * 8 - 1)  # Random bit position
		value ^= (1 << bit_to_flip)  # Flip the bit
		value &= max_value  # Ensure it fits in n bytes

	elif mutation == "add":
		value = (value + random.randint(1, 255)) & max_value  # Add a small value, wrap if needed

	elif mutation == "subtract":
		value = (value - random.randint(1, 255)) & max_value  # Subtract a small value, wrap if needed

	return value

def mutate_tuple(field): # This mutates the thing with fixed size integer...
	length, value = field # Field is actually a tuple of length and the actual value
	value = mutate_integer(value, length)
	return (length, value)


