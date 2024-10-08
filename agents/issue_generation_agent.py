import openai
import os
from dotenv import load_dotenv

load_dotenv()


class IssueGenerationAgent():
    """
    Agent for generating GitHub issues from task descriptions.
    """
    def run(self, tasks):
        """
        Generate GitHub issues from task descriptions.

        Args:
            tasks (list): A list of task descriptions.

        Returns:
            list: A list of generated GitHub issues.
        """
        issues = []
        
        print(tasks)


        # Filter out non-task lines
        task_lines = []
        for line in tasks:
            line = line.strip()
            if line.startswith('## '):
                continue  # Skip phase headers
            if line == '' or line.lower() == 'tasks:':
                continue  # Skip empty lines and 'Tasks:' lines
            if line[0].isdigit() and (line[1] == '.' or line[1] == ')'):
                task_lines.append(line)
            else:
                continue  # Skip other lines

        task_lines = task_lines[:1]

        for task_line in task_lines:
            # Extract task description
            # The task line is expected to be like '1. Task description'
            # We can remove the numbering
            task_description = task_line.split('.', 1)[1].strip()
            prompt = f"""
                Please create a detailed GitHub issue for the following task:

                "{task_description}"

                Include the following sections in your response:

                - **Title**: A concise summary of the task.
                - **Description**: A detailed explanation of what needs to be done.
                - **Acceptance Criteria**: Specific conditions that must be met for the task to be considered complete.
                - **Additional Notes**: Any extra information that might be helpful (e.g., implementation suggestions, dependencies, references to relevant documents).

                Format your response in markdown, and ensure clarity and completeness.
                """

            response = openai.chat.completions.create(
                model=os.getenv('OPENAI_MODEL'),
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for generating detailed GitHub issues from task descriptions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1000,
            )
            # Extract the assistant's reply
            issue_content = response.choices[0].message.content.strip()
            issues.append(issue_content)
        return issues

