from mutator import * # Import the mutation function...
import subprocess












def valid() -> bool:
	result = subprocess.run(["./checkvalidemf.exe", "testfile.emf"], capture_output=True, text=True, check=True)
	output = result.stdout.strip()  # Strip any extra whitespace
	print("output: "+str(output))
	return False



BENCHMARK_COUNT = 10_0

def run_benchmark():
	fh = open("testfile.emf", "rb")
	original_data = fh.read()
	fh.close()

	# Now try to mutate.
	valid_count = 0
	for _ in range(BENCHMARK_COUNT):
		data = copy.deepcopy(original_data)
		mutated_data = fuzz(data) # Try to fuzz.
		# Write to input file.
		fh = open("bench_input.emf", "wb")
		fh.write(mutated_data)
		fh.close()
		if valid():
			valid_count += 1
	print(valid_count / BENCHMARK_COUNT)
	return



if __name__=="__main__":
	run_benchmark()
	exit(0)
