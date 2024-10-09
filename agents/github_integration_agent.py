import os
from github import Github
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()

class GitHubIntegrationAgent():
    """
    Agent for creating GitHub issues from task descriptions.
    """
    def __init__(self, github_token, repo_owner, repo_name):
        """
        Initialize the GitHubIntegrationAgent.

        Args:
            github_token (str): The GitHub token.
            repo_owner (str): The owner of the repository.
            repo_name (str): The name of the repository.
        """
        self.github_token = github_token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_client = Github(self.github_token)
        self.repo = self.github_client.get_repo(f"{self.repo_owner}/{self.repo_name}")

    def create_github_issue(self, issue_content):
        """
        Creates a new issue in the GitHub repository based on the provided content.

        Args:
            issue_content (str): The full content of the issue.

        Returns:
            github.Issue.Issue or None: The created issue object if successful, None otherwise.
        """
        if self.repo is None:
            return None

        try:
            # Parse the content
            lines = issue_content.strip().split('\n')

            # Extract the title
            title = None
            for line in lines:
                if line.startswith('# '):
                    title = line.strip('# ').strip()
                    break
                elif line.startswith('**Title**:'):
                    title = line.split('**Title**:', 1)[1].strip()
                    break

            if not title:
                logger.error("Failed to extract a valid title from the issue content")
                return None

            # Remove the title line from the body
            body_lines = [line for line in lines if not line.startswith('# ') and not line.startswith('**Title**:')]
            body = '\n'.join(body_lines).strip()

            # Create the issue
            issue = self.repo.create_issue(title=title, body=body)
            logger.info(f"Successfully created issue: {issue.title} (#{issue.number})")
            return issue
        except Exception as e:
            logger.error(f"Failed to create issue: {str(e)}")
            return None
