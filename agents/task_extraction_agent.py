import openai
import os
from dotenv import load_dotenv

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
            str: The extracted tasks.
        """
        prompt = f"""
            Extract all tasks from the following PRD:

            {prd_text}

            Please read the following Product Requirements Document (PRD) and extract all possible tasks.
            Organize the tasks under their respective phases and categories as outlined in the PRD.
            For each task, include any sub-tasks or specific implementation details mentioned.
            Also note any additional notes or comments from the product manager like deadlines, dependencies, timeline, etc.
            Return the tasks in a list format.
        """
        response = openai.chat.completions.create(
            model=os.getenv('OPENAI_MODEL'),
            messages=[
                {"role": "system", "content": "You are a helpful assistant for extracting detailed tasks from PRD Markdown files."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2000,
        )
        return response.choices[0].message.content
