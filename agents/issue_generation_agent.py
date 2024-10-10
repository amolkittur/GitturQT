# agents/issue_generation_agent.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()

class IssueGenerationAgent():
    """
    Agent for generating GitHub issues from task descriptions.
    """
    def issue_generation(self, selected_tasks):
        """
        Generate GitHub issues from selected tasks.

        Args:
            selected_tasks (list): A list of selected tasks with their details.

        Returns:
            list: A list of generated GitHub issues.
        """
        issues = []

        for task in selected_tasks:
            phase = task.get('phase', 'N/A')
            task_title = task['task_title']
            task_description = task.get('task_description', '')
            task_additional_input = task.get('additional_input', '')
            subtasks = task.get('selected_subtasks', [])

            if subtasks:
                for subtask in subtasks:
                    subtask_title = subtask['title']
                    subtask_description = subtask.get('description', '')
                    subtask_additional_input = subtask.get('additional_input', '')
                    # Combine additional inputs
                    additional_input = '\n'.join(filter(None, [task_additional_input, subtask_additional_input]))
                    issue_content = self.generate_issue(
                        phase, task_title, task_description, subtask_title, subtask_description, additional_input
                    )
                    issues.append(issue_content)
            else:
                # No subtasks selected, generate issue for the task
                issue_content = self.generate_issue(
                    phase, task_title, task_description, None, None, task_additional_input
                )
                issues.append(issue_content)
        return issues

    def generate_issue(self, phase, task_title, task_description, subtask_title, subtask_description, additional_input):
        """
        Generate an issue for a task or subtask.

        Args:
            phase (str): The phase of the task.
            task_title (str): The title of the task.
            task_description (str): The description of the task.
            subtask_title (str or None): The title of the subtask, if any.
            subtask_description (str or None): The description of the subtask, if any.
            inputs (str or None): The inputs provided for the task or subtask.
            output (str or None): The output expected from the task or subtask.
            additional_input (str or None): Additional input provided by the user.

        Returns:
            str: The generated issue content.
        """
        prompt = f"""
                Please create a detailed GitHub issue for the following:

                Phase: {phase}
                Task Title: {task_title}
                Task Description: {task_description}
                """

        if subtask_title:
            prompt += f"""
                Subtask Title: {subtask_title}
                Subtask Description: {subtask_description}
                """

        if additional_input:
            prompt += f"""
                        Additional Input: {additional_input}
                        """

        prompt += """
                Include the following sections in your response:

                - **Title**: A concise summary of the task.
                - **Description**: A detailed explanation of what needs to be done.
                - **Inputs**: A list of inputs that are required for the task or subtask.
                - **Output**: A list of outputs that are expected from the task or subtask.
                - **Acceptance Criteria**: Specific conditions that must be met for the task to be considered complete.
                - **Additional Notes**: Any extra information that might be helpful (e.g., implementation suggestions, dependencies, references to relevant documents).

                Format your response in markdown, and ensure clarity and completeness.
                Do not include any code fences or additional formatting around the markdown content.
                Acceptance criteria should be a list of specific conditions that must be met for the task to be considered complete.
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
        return issue_content
