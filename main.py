import os
from dotenv import load_dotenv
from agents.task_extraction_agent import TaskExtractionAgent
from agents.issue_generation_agent import IssueGenerationAgent
from agents.github_integration_agent import GitHubIntegrationAgent

load_dotenv()

def get_human_input(prompt):
    """
    Get human input for task selection or approval.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        bool: True if the user approves, False otherwise.
    """
    response = input(prompt)
    return response.strip().lower() in ['yes', 'y']

def main(prd_file_path):
    """
    Main function to run the program.

    Args:
        prd_file_path (str): The path to the PRD file.
    """
    with open(prd_file_path, 'r') as file:
        prd_text = file.read()

    # Initialize agents
    task_agent = TaskExtractionAgent()
    issue_agent = IssueGenerationAgent()
    github_agent = GitHubIntegrationAgent(
        github_token=os.getenv('GITHUB_TOKEN'),
        repo_owner=os.getenv('REPO_OWNER'),
        repo_name=os.getenv('REPO_NAME')
    )

    # Step 1: Extract tasks from PRD
    tasks = task_agent.run(prd_text)
    print("Extracted Tasks:")
    print(tasks)

    # Ask for human input
    proceed = get_human_input("Do you want to proceed with these tasks? (yes/no): ")
    if not proceed:
        print("Process terminated by user.")
        return

    # Step 2: Generate GitHub issues from tasks
    task_list = tasks.split('\n')  # Assuming tasks are separated by newlines
    issues = issue_agent.run(task_list)
    print("Generated Issues:")
    for issue in issues:
        print(issue)

    # Ask for human input
    proceed = get_human_input("Do you approve these issues to be created on GitHub? (yes/no): ")
    if not proceed:
        print("Process terminated by user.")
        return

    # Step 3: Create issues on GitHub
    created_issues = github_agent.create_github_issue(issues)
    print("Created GitHub Issues:")
    for issue in created_issues:
        print(f"Issue URL: {issue.get('html_url')}")

if __name__ == '__main__':
    main('GitturQT.md')