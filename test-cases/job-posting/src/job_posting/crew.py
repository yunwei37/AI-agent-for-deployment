import json
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool, FileReadTool
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI

llm4_mini = ChatOpenAI(model='gpt-4o-mini')
llm4 = ChatOpenAI(model='gpt-4o')

# # Load the LLM configuration from JSON
# with open('config/map_agent_llm.json', 'r') as f:
#     llm_config = json.load(f)

# print(llm_config)

web_search_tool = WebsiteSearchTool()
seper_dev_tool = SerperDevTool()
file_read_tool = FileReadTool(
    file_path='job_description_example.md',
    description='A tool to read the job description example file.'
)

class ResearchRoleRequirements(BaseModel):
    """Research role requirements model"""
    skills: List[str] = Field(..., description="List of recommended skills for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements.")
    experience: List[str] = Field(..., description="List of recommended experience for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements.")
    qualities: List[str] = Field(..., description="List of recommended qualities for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements.")

@CrewBase
class JobPostingCrew:
    """JobPosting crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def research_agent(self) -> Agent:
        # print(llm_config['research_agent'])
        return Agent(
            llm= llm4_mini, # llm_config['research_agent'],
            config=self.agents_config['research_agent'],
            tools=[web_search_tool, seper_dev_tool],
            verbose=True
        )
    
    @agent
    def writer_agent(self) -> Agent:
        # print(llm_config['writer_agent'])
        return Agent(
            llm= llm4, # llm_config['research_agent'],
            config=self.agents_config['writer_agent'],
            tools=[web_search_tool, seper_dev_tool, file_read_tool],
            verbose=True
        )
    
    @agent
    def review_agent(self) -> Agent:
        # print(llm_config['review_agent'])
        return Agent(
            llm= llm4, # llm_config['research_agent'],
            config=self.agents_config['review_agent'],
            tools=[web_search_tool, seper_dev_tool, file_read_tool],
            verbose=True
        )
    
    @task
    def research_company_culture_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_company_culture_task'],
            agent=self.research_agent()
        )

    @task
    def research_role_requirements_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_role_requirements_task'],
            agent=self.research_agent(),
            output_json=ResearchRoleRequirements
        )

    @task
    def draft_job_posting_task(self) -> Task:
        return Task(
            config=self.tasks_config['draft_job_posting_task'],
            agent=self.writer_agent()
        )

    @task
    def review_and_edit_job_posting_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_and_edit_job_posting_task'],
            agent=self.review_agent()
        )

    @task
    def industry_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['industry_analysis_task'],
            agent=self.research_agent(),
            output_file='answer.md',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the JobPostingCrew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
            output_log_file='log.txt',
        )

# Example of creating a JobPostingCrew instance
# job_posting_crew = JobPostingCrew()