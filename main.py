import os
import json
from dotenv import load_dotenv
from agents.task_extraction_agent import TaskExtractionAgent
from agents.issue_generation_agent import IssueGenerationAgent
from agents.github_integration_agent import GitHubIntegrationAgent
from agents.transcript_creation_agent import TranscriptCreationAgent
from agents.prd_creation_agent import MeetingToPRDAgent

load_dotenv()


meeting_transcript_folder = 'docs/meeting_transcripts'
prd_folder = 'docs/prd'
phase_folder = 'docs/phases'

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

def create_transcript():
    transcript_agent = TranscriptCreationAgent()
    audio_file_path = input("Enter the path to the audio file: ")
    transcript = transcript_agent.create_transcript(audio_file_path)
    transcript_name = input("Enter the name of the transcript file (without .md extension): ")
    transcript_name_with_extension = f"{transcript_name}.md"
    with open(os.path.join(meeting_transcript_folder, transcript_name_with_extension), 'w') as file:
        file.write(transcript)
    print(f"Transcript created and saved to {transcript_name_with_extension}")
    return transcript, transcript_name_with_extension

def create_prd(transcript=None, transcript_name=None):
    prd_agent = MeetingToPRDAgent()
    if not transcript:
        transcript_name = input("Enter the name of the transcript file: ")
        transcript_name_with_extension = f"{transcript_name}.md"
        with open(os.path.join(meeting_transcript_folder, transcript_name_with_extension), 'r') as file:
            transcript = file.read()
    prd_text = prd_agent.transcript_to_prd(transcript)
    prd_name = input("Enter the name of the PRD file (without .md extension): ")
    prd_name_with_extension = f"{prd_name}.md"
    with open(os.path.join(prd_folder, prd_name_with_extension), 'w') as file:
        file.write(prd_text)
    print(f"PRD created and saved to {prd_name_with_extension}")
    return prd_text, prd_name_with_extension

def create_phase_list(prd_text=None, prd_name=None):
    task_agent = TaskExtractionAgent()
    if not prd_text:
        prd_name = input("Enter the name of the PRD file (without .md extension): ")
        prd_name_with_extension = f"{prd_name}.md"
        with open(os.path.join(prd_folder, prd_name_with_extension), 'r') as file:
            prd_text = file.read()
    tasks_json = task_agent.task_extraction(prd_text)
    tasks_json_clean = clean_json_string(tasks_json)
    try:
        tasks_dict = json.loads(tasks_json_clean)
        tasks = tasks_dict.get('tasks', [])
    except json.JSONDecodeError as e:
        print("Error parsing tasks JSON:", e)
        return None
    phase_name = input("Enter the name for the phase list file: ")
    with open(os.path.join(phase_folder, phase_name), 'w') as file:
        json.dump(tasks, file, indent=2)
    print(f"Phase list created and saved to {phase_name}")
    
    # Use get_user_task_selection to allow user to select tasks
    selected_tasks = get_user_task_selection(tasks)
    return selected_tasks, phase_name

def create_github_issues(selected_tasks=None, phase_name=None):
    if not selected_tasks:
        phase_name = input("Enter the name of the phase list file: ")
        with open(os.path.join(phase_folder, phase_name), 'r') as file:
            tasks = json.load(file)
        selected_tasks = get_user_task_selection(tasks)
    
    if not selected_tasks:
        print("No tasks selected. Exiting.")
        return

    issue_agent = IssueGenerationAgent()
    issues = issue_agent.issue_generation(selected_tasks)
    print("\nGenerated Issues:")
    for issue in issues:
        print(issue)
        print("-" * 80)

    proceed = input("Do you approve these issues to be created on GitHub? (yes/no): ").strip().lower()
    if proceed not in ['yes', 'y']:
        print("Process terminated by user.")
        return

    github_agent = GitHubIntegrationAgent(
        github_token=os.getenv('GITHUB_TOKEN'),
        repo_owner=os.getenv('REPO_OWNER'),
        repo_name=os.getenv('REPO_NAME')
    )

    for issue_content in issues:
        issue = github_agent.create_github_issue(issue_content)
        if issue:
            print(f"Issue created: {issue.html_url}")
        else:
            print("Failed to create issue.")

def main():
    transcript = None
    transcript_name = None
    prd_text = None
    prd_name = None
    selected_tasks = None
    phase_name = None

    # Step 1: Create transcript
    if input("Do you want to create a transcript from an audio file? (yes/no): ").strip().lower() in ['yes', 'y']:
        transcript, transcript_name = create_transcript()

    # Step 2: Create PRD
    if input("Do you want to create a PRD from the transcript? (yes/no): ").strip().lower() in ['yes', 'y']:
        prd_text, prd_name = create_prd(transcript, transcript_name)

    # Step 3: Create phase list and select tasks
    if input("Do you want to create a phase list and select tasks? (yes/no): ").strip().lower() in ['yes', 'y']:
        selected_tasks, phase_name = create_phase_list(prd_text, prd_name)

    # Step 4: Create GitHub issues
    if input("Do you want to create GitHub issues for the selected tasks? (yes/no): ").strip().lower() in ['yes', 'y']:
        create_github_issues(selected_tasks, phase_name)

if __name__ == '__main__':
    main()
