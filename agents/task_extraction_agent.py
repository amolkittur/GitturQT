import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

class TaskExtractionAgent():
    """
    Agent for extracting tasks from a PRD.
    """
    def run(self, prd_text):
        """
        Extract tasks from a PRD.

        Args:
            prd_text (str): The PRD text.

        Returns:
            list: A list of tasks with their details.
        """
        prompt = f"""
        Please read the following Product Requirements Document (PRD) and extract all possible tasks.
        Organize the tasks under their respective phases and categories as outlined in the PRD.
        For each task, include any sub-tasks or specific implementation details mentioned.
        Return the tasks in a structured JSON format with the following fields:

        - 'phase': The phase under which the task falls.
        - 'task_title': The title of the task.
        - 'task_description': A brief description of the task.
        - 'subtasks': A list of subtasks, each with a 'title' and 'description'.

        Ensure the JSON is properly formatted and can be parsed by Python's json.loads() method.

        **Important**: Do not include any markdown formatting, code fences, or additional text. Only return the pure JSON.

        PRD Content:
        {prd_text}
        """
        response = openai.chat.completions.create(  
            model=os.getenv('OPENAI_MODEL'),
            messages=[
                {"role": "system", "content": "You are an assistant that extracts tasks from PRDs and returns them in structured JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2000,
        )
        tasks_json = response.choices[0].message.content.strip()
        return tasks_json  # This should be a JSON string
