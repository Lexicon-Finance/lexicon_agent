from typing import Optional
from dotenv import load_dotenv
import openai
from tenacity import retry, stop_after_attempt, wait_exponential
import os

class LLMHandler:
    def __init__(self, model: Optional[str] = None):
        """
        Initialize the LLM handler.
        
        Args:
            model: The OpenAI model to use. If None, uses environment variable or default.
        """
        # Load environment variables
        load_dotenv()
        
        # Get API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        # Set model from args, env, or default
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
        
        # Initialize the OpenAI client
        openai.api_key = api_key
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def analyze(self, prompt: str) -> str:
        """
        Analyze a prompt using the LLM and return the response as a string.
        
        Args:
            prompt: The prompt to analyze
            
        Returns:
            The LLM's response as a string
                
        Raises:
            Exception: If LLM analysis fails after retries
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
                
        except Exception as e:
            raise Exception(f"LLM analysis failed: {str(e)}")