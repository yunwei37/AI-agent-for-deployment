import os
from gen import ai_generate_content

def read_file(file_path):
    """Read the content of the input file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    # Read the content from the markdown files
    cpu_guide = read_file('manager/cpu-inference-guide.md')
    gpu_guide = read_file('manager/gpu-resource-guide.md')
    system_report = read_file('detect_environment/report.md')

    # Construct the prompt for the AI model
    prompt = (
        "Based on the following system report and inference guides, "
        "generate a report on what model can be chosen and where to deploy it:\n\n"
        "System Report:\n"
        f"{system_report}\n\n"
        "CPU Inference Guide:\n"
        f"{cpu_guide}\n\n"
        "GPU Resource Guide:\n"
        f"{gpu_guide}\n"
    )

    # Generate the report using the AI model
    report = ai_generate_content(prompt)

    # Output the report
    output_file = 'manager/deployment_recommendation_report.md'
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(report)

    print(f"Deployment recommendation report generated and saved to '{output_file}'.")

if __name__ == "__main__":
    main()
