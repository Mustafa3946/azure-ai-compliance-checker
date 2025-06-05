"""
llm_assist.py

Provides functions to generate executive summaries of compliance scan results using either a local LLaMA model or OpenAI's GPT models.
Allows cost-effective local summarization by default, with optional OpenAI integration.

Functions:
    - generate_summary_with_openai: Uses OpenAI API to summarize compliance scan results.
    - generate_summary_with_local_llama: Uses a local LLaMA model to summarize compliance scan results.
"""

import os
import json

# Optional import for local LLaMA support
try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

from openai import OpenAI


def generate_summary_with_openai(scan_results: dict, model="gpt-3.5-turbo"):
    """
    Generate an executive summary of compliance scan results using OpenAI.
    Returns a summary string or an error message.
    """
    # Initialize the OpenAI client using environment variable for API key
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = (
        "You are a compliance and governance expert. "
        "Write a one-paragraph executive summary of the Azure compliance scan results provided below. "
        "Use formal plain English with no formatting — do not use markdown, bullet points, headings, or tables. "
        "Just a professional paragraph summarizing the results.\n\n"
        f"{json.dumps(scan_results, indent=2)}"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a compliance and governance expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI summary failed: {str(e)}"

def generate_summary_with_local_llama(scan_results: dict, model_path=r".\models\llama-2-7b.Q4_K_M.gguf"):
    """
    Generate an executive summary of compliance scan results using a local LLaMA model.
    Returns a summary string or an error message.
    """
    if Llama is None:
        return "llama-cpp-python is not installed. Please install it with `pip install llama-cpp-python` to use local models."

    prompt = (
        "You are a compliance and governance expert. "
        "Write a one-paragraph executive summary of the Azure compliance scan results provided below. "
        "Use formal plain English with no formatting — do not use markdown, bullet points, headings, or tables. "
        "Just a professional paragraph summarizing the results.\n\n"
        f"{json.dumps(scan_results, indent=2)}"
    )

    try:
        llama = Llama(model_path=model_path)
        response = llama(prompt, max_tokens=300, temperature=0.5)
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Local LLaMA summary failed: {str(e)}"
