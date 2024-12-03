import os
import json
from gen_struct import read_file, ai_generate_content

def generate_agent_mapping(models_desc, app_desc, agents_desc):
    # Read the routing template
    template = read_file("manager/routing.md")
    
    # Replace placeholders in the template
    prompt = template.replace("{models-description}", models_desc)\
                    .replace("{application-description}", app_desc)\
                    .replace("{agents-description}", agents_desc)

    # Define a schema for mapping agents to LLMs using a list structure
    schema = {
        "type": "object",
        "properties": {
            "mappings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "agent": {"type": "string"},
                        "model": {"type": "string"}
                    },
                    "required": ["agent", "model"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["mappings"],
        "additionalProperties": False
    }

    # Generate the mapping using the AI
    result = ai_generate_content(prompt, schema)
    
    # Convert the list format to the desired object format
    mapping = {item["agent"]: {"model": item["model"]} for item in result["mappings"]}
    return mapping

def main():
    # Example inputs
    models_desc = """
    Available models:
    - gpt-4o: Most capable model, best for complex reasoning
    - gpt-4o-mini: Balanced performance and cost
    """

    app_desc = """
    An AI application for processing job postings and generating relevant content.
    """

    agents_desc = """
    - research_agent: Analyzes job requirements and market trends
    - writer_agent: Generates job posting content
    - review_agent: Reviews and refines the generated content
    """

    try:
        # Generate the mapping
        mapping = generate_agent_mapping(models_desc, app_desc, agents_desc)
        
        # Save the result
        output_dir = "manager"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "map_agent_llm.json")
        
        with open(output_path, "w") as f:
            json.dump(mapping, f, indent=4)
            
        print(f"Successfully generated mapping and saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 