from crewai_tools import BaseTool
import subprocess


class BashExecutionTool(BaseTool):
    name: str = "Bash Command Executor"
    description: str = (
        "A tool that executes bash commands and returns their output. "
        "Provide the bash command as a string argument, and it will return the command's output. "
        "Use this tool when you need to run shell commands and get their results."
    )

    def _run(self, command: str) -> str:
        try:
            # Execute the command and capture output
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.stderr}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
