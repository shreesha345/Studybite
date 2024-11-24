import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import json
from dotenv import load_dotenv
import os
load_dotenv()
# from kaggle_secrets import UserSecretsClient
# user_secrets = UserSecretsClient()

class TranscriptBestPartsExtractor:
    def __init__(self, google_api_key):
        # Configure Gemini
        genai.configure(api_key=google_api_key)
        
        # Initialize Gemini model for chat
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-002",
            temperature=0.7,
            google_api_key=google_api_key
        )

    def extract_best_parts(self, transcript_file, topic, num_segments=2):
        """Extract the most important segments using Gemini from transcript.json"""
        
        # Read the transcript file
        try:
            with open(transcript_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        except Exception as e:
            raise ValueError(f"Error reading transcript file: {str(e)}")

        prompt_template = """You are an AI trained to identify the most important and valuable parts of a transcript.
        
        Analyze these transcript segments and select exactly {num_segments} most important parts that provide the most value about:
        {topic}
        Transcript segments:
        {segments}
        
        Requirements:
        1. Return ONLY a JSON array with the {num_segments} best segments
        2. Each object must have exactly these keys: "start_time", "end_time", "description", "duration"
        3. Keep the exact original timing information and text
        4. Do not modify or summarize the text content
        5. Include only complete thoughts/segments
        6. Format as a valid JSON array
        7. Do not add any extra text or explanations
        8. the clips should be min 50 seconds in duration
        9. the clip should be less then 60 seconds
        
        Return only the JSON array, nothing else."""
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        
        # Create JSON string of segments
        segments_str = json.dumps(json_data, indent=2)
        
        # Create messages
        messages = prompt.format_messages(
            segments=segments_str,
            topic=topic,
            num_segments=num_segments
        )
        
        # Get response from Gemini
        response = self.llm.invoke(messages)
        
        # Extract JSON from response
        try:
            # Find the JSON array in the response
            response_text = response.content
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")
                
            json_str = response_text[start_idx:end_idx]
            best_segments = json.loads(json_str)
            
            # Validate each segment
            for segment in best_segments:
                # Check required fields
                required_fields = ["start_time", "end_time", "description", "duration"]
                if not all(field in segment for field in required_fields):
                    raise ValueError("Missing required fields in segment")
                
                # Validate types
                if not isinstance(segment["start_time"], (int, float)):
                    raise ValueError("start_time must be a number")
                if not isinstance(segment["end_time"], (int, float)):
                    raise ValueError("end_time must be a number")
                if not isinstance(segment["duration"], (int, float)):
                    raise ValueError("duration must be a number")
                if not isinstance(segment["description"], str):
                    raise ValueError("description must be a string")
                    
            # Save the results to a new file
            output_file = "best_segments.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(best_segments, f, indent=2, ensure_ascii=False)
                
            print(f"Best segments saved to {output_file}")
            return best_segments
            
        except json.JSONDecodeError:
            raise ValueError("Failed to parse Gemini response as JSON")

def gemini_insights(topic):
    # Your Google API key
    # GOOGLE_API_KEY = secret_value_0 = user_secrets.get_secret("GEMINI_API_KEY")
    GOOGLE_API_KEY = secret_value_0 = os.getenv("GEMINI_API_KEY")
    
    # Initialize extractor
    extractor = TranscriptBestPartsExtractor(GOOGLE_API_KEY)
    
    # Process transcript and get best parts
    best_segments = extractor.extract_best_parts("transcript.json", topic, num_segments=3)
    
    # Print results
    print("\nBest transcript segments:")
    print(json.dumps(best_segments, indent=2))
    return (json.dumps(best_segments, indent=2))

if __name__ == "__main__":
    gemini_insights()