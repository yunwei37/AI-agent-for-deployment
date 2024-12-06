import os
import subprocess

def main():
    print("Welcome to the AI Agent Deployment Script!")
    
    # Ask user for the application path
    app_path = input("Please enter the path to your LLM application: ")
    
    # Generate description
    print("Generating application description...")
    description_command = f"python manager/gen_llm_app_description.py {app_path}"
    subprocess.run(description_command, shell=True, text=True)
    
    # Print the generated descriptions
    desc_file = f"{os.path.splitext(app_path)[0]}_desc.py"
    print("\nGenerated Application Description:")
    print("==================================")
    with open(desc_file, "r") as file:
        print(file.read())
    print("==================================\n")
    
    # Ask user to confirm
    confirm = input("Description generated. Do you want to continue? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Exiting the script.")
        return
    
    # Change directory and detect environment
    os.chdir("detect_environment")
    print("Detecting environment...")
    subprocess.run("poetry run detect_environment", shell=True, text=True)
    
    # Save report
    report_path = "detect_environment/report.md"
    print(f"Environment detection report saved to '{report_path}'.")

    os.chdir("..")
    # print the report
    with open(report_path, "r") as file:
        print(file.read())
    print("--------------------------------")
    
    # Generate deployment guide
    print("\nGenerating deployment guide...")
    subprocess.run("python manager/gen_deployment_guide.py", shell=True, text=True)
    
    # Print the deployment guide
    with open("manager/deployment_recommendation_report.md", "r") as file:
        print(file.read())
    print("--------------------------------")

    # Ask user about local deployment
    local_deploy = input("Do you want to deploy the model locally? (yes/no): ")
    if local_deploy.lower() == 'yes':
        print("\nInitiating local deployment...")
        subprocess.run("python manager/local_deploy.py", shell=True, text=True)
    
    # Generate Ray code
    print("\nGenerating Ray-based implementation...")
    ray_command = f"python manager/generate_ray_code.py {app_path}"
    subprocess.run(ray_command, shell=True, text=True)
    
    ray_file = os.path.splitext(app_path)[0] + "_ray.py"
    
    # print the generated ray code
    with open(ray_file, "r") as file:
        print(file.read())
    print("--------------------------------")
    
    # ask user to confirm and run it
    run_it = input("Do you want to run the Ray-based implementation? (yes/no): ")
    if run_it.lower() == 'yes':
        subprocess.run(f"python {ray_file}", shell=True)
    
    print("Process completed successfully.")

if __name__ == "__main__":
    main()
