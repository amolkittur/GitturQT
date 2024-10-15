import openai
import os
from dotenv import load_dotenv
from typing import Dict, Any
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MeetingToPRDAgent:
    """
    Agent for creating a PRD from a meeting transcript.
    """
    def __init__(self):
        # Load environment variables    
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        if not openai.api_key:
            raise ValueError("OpenAI API key not found. Please check your .env file.")

    def transcript_to_prd(self, transcript: str) -> str:
        prompt = f"""
        Convert the following meeting transcript into a comprehensive, industry-standard Product Requirements Document (PRD):

        {transcript}

        The PRD should include the following sections:
        1. Introduction
        2. Product Overview
        3. Objectives and Goals
        4. Target Audience
        5. Features and Requirements
        6. User Stories
        7. Non-Functional Requirements
        8. Constraints and Limitations
        9. Milestones and Timeline
        10. Success Metrics
        """

        try:
            response = openai.chat.completions.create(
                model=os.getenv('OPENAI_MODEL'),
                messages=[
                    {"role": "system", "content": "You are a product manager tasked with creating a PRD from a meeting transcript."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=2000,
            )

            prd = response.choices[0].message.content.strip()
            return prd

        except Exception as e:
            logger.error(f"Error processing meeting: {str(e)}")
            return {"error": str(e)}

    def process_meeting(self, transcript: str) -> Dict[str, Any]:
        try:
            prd = self.transcript_to_prd(transcript)
            return {
                "prd": prd
            }
        except Exception as e:
            logger.error(f"Error processing meeting: {str(e)}")
            return {"error": str(e)}
