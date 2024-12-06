import os
import sys
from gen import ai_generate_content

def read_file(file_path):
    """Read the content of the input file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_descriptions(source_code):
    """
    Use AI to generate the app description and agent descriptions
    from the given LLM application source code.
    """
    prompt = (
        "Analyze the following Python source code of an LLM application. "
        "Generate two outputs:\n"
        "1. A brief description of the application, summarizing its purpose and functionality (app_desc).\n"
        "2. A list of agents or components used in the application, each with a brief description of its role (agents_desc). "
        "Format the output as:\n\n"
        "app_desc = \"\"\"\n<Brief description of the application>\n\"\"\"\n\n"
        "agents_desc = \"\"\"\n"
        "- <agent_name>: <agent_role_description>\n"
        "- ...\n"
        "\"\"\"\n\n"
        "Source Code:\n"
        f"{source_code}"
    )
    
    # Use AI to generate descriptions
    descriptions = ai_generate_content(prompt)
    return descriptions

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_desc.py <source_file>")
        sys.exit(1)

    input_file = sys.argv[1]  # The source file containing the LLM application code
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(1)
    print(f"Generating descriptions for {input_file}...")
    # Read the source code
    source_code = read_file(input_file)

    # Generate the app and agents descriptions
    descriptions = generate_descriptions(source_code)

    # Output the descriptions
    output_file = os.path.splitext(input_file)[0] + "_desc.py"
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(descriptions)

    print(f"App and agents descriptions written to '{output_file}'.")

if __name__ == "__main__":
    main()
