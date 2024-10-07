import os
import openai
from dotenv import load_dotenv
import json
import re
import logging
from github import Github, GithubException

# Load environment variables
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPO')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize GitHub client
github_account = Github(GITHUB_TOKEN)

def get_github_repo():
    """
    Logs into the GitHub account and returns the repository object.
    """
    try:
        repo = github_account.get_repo(REPO_NAME)
        logger.info(f"Successfully accessed repository: {REPO_NAME}")
        return repo
    except Exception as e:
        logger.error(f"Failed to access repository '{REPO_NAME}': {str(e)}")
        return None

def extract_json_from_response(content):
    """
    Extracts JSON string from a response containing Markdown code blocks.
    """
    pattern = r'json\s*(\[\s*\{.*?\}\s*\])\s*'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding failed: {e}")
            return None
    else:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.error("No JSON block found and direct parsing failed.")
            return None

def get_task_extraction_prompt(markdown_content):
    """
    Generates the prompt for task extraction.
    """
    return f"""
    You are an assistant that extracts tasks from a Markdown Product Requirement Document (PRD). For each task, provide the following details in JSON format without any code blocks or Markdown formatting:
    - Issue Title: A short, descriptive title for the task.
    - Description: A detailed description of the task.
    - Inputs: Any inputs required for the task.
    - Expected Output: The expected result or behavior after completing the task.
    - Labels: Relevant labels for the task (e.g., bug, feature, enhancement).
    - Assignees: GitHub usernames to assign the task to (if any).
    - Attachments: Links or references to relevant documents or designs.

    Markdown Content:
    {markdown_content}

    Extracted Tasks JSON:
    """

def extract_tasks(markdown_content):
    """
    Extracts tasks from a Markdown PRD and returns them in JSON format.
    """
    prompt = get_task_extraction_prompt(markdown_content)
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for extracting detailed tasks from PRD Markdown files."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=2000,
    )
    content = response.choices[0].message.content
    return parse_ai_response(content)

def parse_ai_response(content):
    """
    Parses the AI response and returns the extracted tasks.
    """
    try:
        if content.strip().startswith('[') and content.strip().endswith(']'):
            return json.loads(content)
        else:
            return extract_json_from_response(content)
    except json.JSONDecodeError:
        logger.error("Failed to parse JSON from AI response.")
        return []

def get_issue_elaboration_prompt(task):
    """
    Generates the prompt for issue elaboration.
    """
    return f"""
    Create a detailed GitHub issue with the following information:

    Title: {task.get('Issue Title', 'Untitled Task')}
    Description: {task.get('Description', 'No description provided.')}
    Motivation: {task.get('Motivation', '')}
    Acceptance Criteria: {task.get('Acceptance Criteria', '')}
    Inputs: {task.get('Inputs', 'No inputs specified.')}
    Expected Output: {task.get('Expected Output', 'No expected output specified.')}
    Additional Notes: {task.get('Additional Notes', '')}

    Please format the issue using Markdown, including sections for Summary, Motivation, Acceptance Criteria, Inputs, Expected Output, Additional Notes, and Attachments.
    """

def elaborate_issue_with_chatgpt(task):
    """
    Uses ChatGPT to elaborate on the issue details.
    """
    prompt = get_issue_elaboration_prompt(task)
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for extracting detailed tasks from PRD Markdown files."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
            n=1,
            stop=None
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error communicating with OpenAI API: {str(e)}")
        return None

def construct_issue_body(task, use_chatgpt=True):
    """
    Constructs the issue body, optionally using ChatGPT for elaboration.
    """
    if use_chatgpt:
        issue_body = elaborate_issue_with_chatgpt(task)
        try:
            if issue_body.strip().startswith('[') and issue_body.strip().endswith(']'):
                return json.loads(issue_body)
            else:
                return extract_json_from_response(issue_body)
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON from AI response.")
            return None
    else:
        return task

def filter_labels_and_assignees(repo, labels, assignees):
    """
    Filters labels and assignees based on repository permissions.
    """
    existing_labels = {label.name for label in repo.get_labels()}
    filtered_labels = [label for label in labels if label in existing_labels]
    
    missing_labels = set(labels) - existing_labels
    if missing_labels:
        logger.warning(f"The following labels do not exist in the repository and will be ignored: {missing_labels}")

    existing_assignees = {user.login for user in repo.get_collaborators()}
    assignees_cleaned = [user.lstrip('@') for user in assignees]
    filtered_assignees = [user for user in assignees_cleaned if user in existing_assignees]

    missing_assignees = set(assignees_cleaned) - existing_assignees
    if missing_assignees:
        logger.warning(f"The following assignees are not collaborators and will be ignored: {missing_assignees}")

    return filtered_labels, filtered_assignees

def create_github_issue(task, repo, use_chatgpt=True):
    """
    Creates a GitHub issue based on the provided task dictionary.
    """
    issue_title = task.get('Issue Title', 'Untitled Task')
    issue_body = construct_issue_body(task, use_chatgpt)
    
    if issue_body is None:
        return None

    try:
        filtered_labels, filtered_assignees = filter_labels_and_assignees(repo, task.get('Labels', []), task.get('Assignees', []))

        issue = repo.create_issue(
            title=issue_title,
            body=issue_body,
            labels=filtered_labels,
            assignees=filtered_assignees
        )

        logger.info(f"Issue created successfully: {issue.html_url}")
        return issue.html_url

    except GithubException as e:
        logger.error(f"GitHub API error occurred: {e.data.get('message', str(e))}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred while creating the issue: {str(e)}")
        return None

def main():
    repo = get_github_repo()
    if repo is None:
        return

    with open("prd.md", "rb") as file:
        markdown_content = file.read().decode('utf-8')
    
    tasks = extract_tasks(markdown_content)
    
    for task in tasks:
        issue_url = create_github_issue(task, repo, use_chatgpt=True)
        if issue_url:
            print(f"Created issue: {issue_url}")

if __name__ == "__main__":
    main()