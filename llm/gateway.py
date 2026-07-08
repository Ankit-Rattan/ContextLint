import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from the .env file
load_dotenv()

class LLMGateway:
    def __init__(self, provider: str = "gemini"):
        self.provider = provider.lower()
        
        # Initialize the Gemini client if selected
        if self.provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY is missing from the .env file.")
            
            # The new Client() automatically picks up GEMINI_API_KEY from the environment
            self.gemini_client = genai.Client()

    def generate_optimized_prompt(self, compiled_payload: dict) -> str:
        """
        Routes the compiled payload to the correct LLM provider and returns the string response.
        """
        if self.provider == "gemini":
            return self._call_gemini(compiled_payload)
        else:
            raise NotImplementedError(f"Provider '{self.provider}' is not yet implemented.")

    def _call_gemini(self, payload: dict) -> str:
        """
        Private method to handle the Gemini API call using the new google-genai SDK.
        """
        system_instruction = payload.get("system_instruction", "")
        user_content = payload.get("user_payload", "")
        
        # We use gemini-2.5-flash as it is fast, highly capable, and has a generous free tier.
        model_name = "gemini-2.5-flash"
        
        try:
            # Configure the request to strictly follow the system instructions
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2, # Low temperature for structured, predictable markdown output
            )
            
            response = self.gemini_client.models.generate_content(
                model=model_name,
                contents=user_content,
                config=config
            )
            
            return response.text
            
        except Exception as e:
            return f"Error calling Gemini API: {str(e)}"