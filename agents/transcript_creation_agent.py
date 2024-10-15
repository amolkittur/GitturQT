import openai
import os
from dotenv import load_dotenv
from pydub import AudioSegment


load_dotenv()

class TranscriptCreationAgent():
    """
    Agent for creating a transcript from a meeting.
    """
    
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB in bytes
        self.MAX_DURATION = 10 * 60 * 1000  # 10 minutes in milliseconds
    
    def process_audio_file(self, file_path):
        """
        Check the input file format, convert to MP3 if necessary, and create a transcript.
        """
        # Check file format
        file_format = self.get_file_format(file_path)
        
        if file_format != 'mp3':
            mp3_file_path = self.convert_to_mp3(file_path, file_format)
        else:
            mp3_file_path = file_path
        
        # Create transcript using OpenAI Whisper
        transcript = self.create_transcript(mp3_file_path)
        
        return transcript
    
    def get_file_format(self, file_path):
        """
        Determine the format of the input file.
        """
        _, file_extension = os.path.splitext(file_path)
        return file_extension[1:].lower()
    
    def convert_to_mp3(self, file_path, file_format):
        """
        Convert the input file to MP3 format.
        """
        audio = AudioSegment.from_file(file_path, format=file_format)
        mp3_file_path = file_path.rsplit('.', 1)[0] + '.mp3'
        audio.export(mp3_file_path, format="mp3")
        return mp3_file_path
    
    def split_audio(self, mp3_file_path):
        """
        Split the audio file into smaller chunks if it exceeds the size or duration limit.
        """
        audio = AudioSegment.from_mp3(mp3_file_path)
        chunks = []
        
        if len(audio) > self.MAX_DURATION or os.path.getsize(mp3_file_path) > self.MAX_FILE_SIZE:
            chunk_length = min(self.MAX_DURATION, len(audio))
            for i in range(0, len(audio), chunk_length):
                chunk = audio[i:i+chunk_length]
                chunk_path = f"{mp3_file_path[:-4]}_chunk_{i//chunk_length}.mp3"
                chunk.export(chunk_path, format="mp3")
                chunks.append(chunk_path)
        else:
            chunks.append(mp3_file_path)
        
        return chunks
    
    def create_transcript(self, mp3_file_path):
        """
        Create a transcript from the MP3 file using OpenAI Whisper.
        Handle large files by splitting them into smaller chunks.
        """
        chunks = self.split_audio(mp3_file_path)
        full_transcript = ""
        
        for chunk in chunks:
            with open(chunk, "rb") as audio_file:
                transcript = openai.audio.transcriptions.create(model="whisper-1", file=audio_file)
            full_transcript += transcript.text + " "
            
            # Remove temporary chunk file if it's not the original file
            if chunk != mp3_file_path:
                os.remove(chunk)
        
        return full_transcript.strip()
