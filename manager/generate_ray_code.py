import os
import sys
from gen import ai_generate_content

def read_file(file_path):
    """Read the content of the input file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    """Write the modified content to the output file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def convert_to_ray(content):
    """
    Use AI to rewrite the Python source code to leverage Ray for scheduling, orchestration,
    and parallel computing, following the provided prompt instructions.
    """
    prompt = (
        "Rewrite the following Python source code to leverage Ray for scheduling, "
        "orchestration, and parallel computing. Ensure tasks like model loading, "
        "preprocessing, inference, and postprocessing are distributed across Ray actors "
        "or tasks, maximizing parallelism. Optimize the implementation for scalability and "
        "fault tolerance while maintaining the same functional output.\n\n"
        f"Original Code:\n{content}"
    )

    # Generate the Ray-converted code using AI
    converted_code = ai_generate_content(prompt)
    return converted_code

def main():
    if len(sys.argv) != 2:
        print("Usage: python tool.py <source_file>")
        sys.exit(1)

    input_file = sys.argv[1]  # The original Python source file passed as an argument
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(1)

    output_file = os.path.splitext(input_file)[0] + "_ray.py"  # Generate output file name

    # Read the original source code
    original_content = read_file(input_file)

    # Convert the source code to use Ray
    ray_converted_content = convert_to_ray(original_content)

    # Write the converted code to the output file
    write_file(output_file, ray_converted_content)

    print(f"Ray-converted code written to '{output_file}'.")

if __name__ == "__main__":
    main()
