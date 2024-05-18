import os


class UniqueInt:
    @staticmethod
    def processFile(inputFilePath, outputFilePath):
        print(f"Processing file: {inputFilePath}")
        unique_integers = UniqueInt.readUniqueIntegers(inputFilePath)
        sorted_integers = UniqueInt.sortIntegers(unique_integers)
        UniqueInt.writeOutput(outputFilePath, sorted_integers)
        print(f"Output written to: {outputFilePath}")

    @staticmethod
    def readUniqueIntegers(inputFilePath):
        seen = [False] * 2047  # for range -1023 to 1023
        offset = 1023
        unique_integers = []

        with open(inputFilePath, 'r') as file:
            for line in file:
                items = line.strip().split()

                if len(items) != 1:
                    continue

                item = items[0]

                if item.lstrip('-').isdigit():
                    num = int(item)

                    if -1023 <= num <= 1023 and not seen[num + offset]:
                        seen[num + offset] = True
                        unique_integers.append(num)

        return unique_integers

    @staticmethod
    def sortIntegers(integers):
        # Implementing a simple insertion sort
        for i in range(1, len(integers)):
            key = integers[i]
            j = i - 1
            while j >= 0 and key < integers[j]:
                integers[j + 1] = integers[j]
                j -= 1
            integers[j + 1] = key
        return integers

    @staticmethod
    def writeOutput(outputFilePath, sorted_integers):
        with open(outputFilePath, 'w') as file:
            for num in sorted_integers:
                file.write(f"{num}\n")


# Function to process all files in sample_inputs directory recursively
def process_all_files():
    input_dir = "//Users/macbook/Desktop/Data Structure and Algorithms/dsa/hw01/sample_inputs/"
    output_dir = "/Users/macbook/Desktop/Data Structure and Algorithms/dsa/hw01/sample_results/"

    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith(".txt"):
                input_path = os.path.join(root, filename)
                # Create output path based on relative path from input directory
                rel_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, f"{rel_path}_results.txt")

                # Ensure the output directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                UniqueInt.processFile(input_path, output_path)
                print(f"Processed {filename} to {output_path}")


if __name__ == "__main__":
    process_all_files()
    print("Processing completed.")
