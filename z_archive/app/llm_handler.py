import openai
import re
from app.config import OPENAI_API_KEY

def call_llm(prompt):
    """
    Calls OpenAI's LLM with the given prompt.
    """
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=200
    )
    return response["choices"][0]["text"]

def parse_llm_match_output(llm_response):
    """
    Parses LLM response to extract match score and explanation.
    """
    match_score = None
    explanation = None

    match = re.search(r'Match Score:\s*(\d+)%', llm_response)
    if match:
        match_score = int(match.group(1))

    explanation_match = re.search(r'Explanation:\s*"(.*?)"', llm_response, re.DOTALL)
    if explanation_match:
        explanation = explanation_match.group(1)

    return {
        "match_score": match_score,
        "explanation": explanation or "No explanation provided."
    }
