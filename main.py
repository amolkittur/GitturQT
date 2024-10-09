import os
import json
from dotenv import load_dotenv
from agents.task_extraction_agent import TaskExtractionAgent
from agents.issue_generation_agent import IssueGenerationAgent
from agents.github_integration_agent import GitHubIntegrationAgent

load_dotenv()

def clean_json_string(json_string):
    """
    Remove code fences and whitespace from the JSON string.

    Args:
        json_string (str): The raw JSON string.

    Returns:
        str: The cleaned JSON string.
    """
    # Remove code fences
    if json_string.startswith('```') and json_string.endswith('```'):
        json_string = json_string[3:-3].strip()
    # Remove possible language hints like ```json
    if json_string.startswith('json\n'):
        json_string = json_string[5:].strip()
    return json_string

def get_user_task_selection(tasks):
    """
    Present tasks and subtasks to the user and allow selection.

    Args:
        tasks (list): A list of tasks with their details.

    Returns:
        list: A list of selected tasks and subtasks.
    """
    selected_tasks = []
    print("\nPlease select the tasks/subtasks you want to create GitHub issues for:")
    for i, task in enumerate(tasks):
        print(f"\nTask {i+1}: {task['task_title']} (Phase: {task['phase']})")
        print(f"Description: {task['task_description']}")
        select_task = input("Do you want to create an issue for this task? (yes/no): ").strip().lower()
        task_selected = select_task in ['yes', 'y']
        if task_selected:
            # Proceed to subtasks
            subtasks = task.get('subtasks', [])
            selected_subtasks = []
            if subtasks:
                print("\nThis task has the following subtasks:")
                for j, subtask in enumerate(subtasks):
                    print(f"  Subtask {j+1}: {subtask['title']}")
                    print(f"  Description: {subtask['description']}")
                    select_subtask = input("    Do you want to create an issue for this subtask? (yes/no): ").strip().lower()
                    subtask_selected = select_subtask in ['yes', 'y']
                    if subtask_selected:
                        # Ask for additional input for the subtask
                        add_input = input("""   Do you want to provide additional transcript for this subtask? 
                                                if yes provide the path to the transcript(txt file) (yes/no):""").strip().lower()
                        if add_input in ['yes', 'y']:
                            file_path = input("    Enter the path to the transcript(txt file): ")
                            with open(file_path, 'r') as file:
                                transcript = file.read()
                            subtask['transcript'] = transcript
                        add_input = input("""   Do you want to provide additional document for this subtask? 
                                                if yes provide the web link to the document (yes/no):""").strip().lower()
                        if add_input in ['yes', 'y']:
                            additional_input = input("    Enter the web link to the document: ")
                            subtask['document'] = additional_input
                        add_input = input("""   Do you want to provide additional prompt for this subtask? 
                                                if yes provide the prompt (yes/no):""").strip().lower()
                        if add_input in ['yes', 'y']:
                            additional_input = input("    Enter additional input: ")
                            subtask['prompt'] = additional_input
                        else:
                            subtask['prompt'] = ''
                        selected_subtasks.append(subtask)
            task['task_selected'] = True
            task['selected_subtasks'] = selected_subtasks
            selected_tasks.append(task)
        else:
            # User selected 'no' for the task; do not show subtasks
            continue
    return selected_tasks

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
    tasks_json = task_agent.run(prd_text)
    tasks_json_clean = clean_json_string(tasks_json)
    try:
        tasks_dict = json.loads(tasks_json_clean)
        tasks = tasks_dict.get('tasks', [])
    except json.JSONDecodeError as e:
        print("Error parsing tasks JSON:", e)
        return

    # Step 2: Allow user to select tasks/subtasks
    selected_tasks = get_user_task_selection(tasks)
    if not selected_tasks:
        print("No tasks selected. Exiting.")
        return

    # Optional: Allow user to provide additional inputs for each selected task
    for task in selected_tasks:
        print(f"\nFor task: {task['task_title']}")
        add_input = input("Do you want to provide additional transcript, document, or prompt? (yes/no): ").strip().lower()
        if add_input in ['yes', 'y']:
            additional_input = input("Enter additional input: ")
            task['additional_input'] = additional_input

    # Step 3: Generate GitHub issues from selected tasks
    issues = issue_agent.run(selected_tasks)
    print("\nGenerated Issues:")
    for issue in issues:
        print(issue)
        print("-" * 80)

    # Ask for human input
    proceed = input("Do you approve these issues to be created on GitHub? (yes/no): ").strip().lower()
    if proceed not in ['yes', 'y']:
        print("Process terminated by user.")
        return

    # Step 4: Create issues on GitHub
    for issue_content in issues:
        issue = github_agent.create_github_issue(issue_content)
        if issue:
            print(f"Issue created: {issue.html_url}")
        else:
            print("Failed to create issue.")

if __name__ == '__main__':
    main('docs/prd/GitturQT.md')
