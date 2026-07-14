"""
factory/teams/llm_base.py

A highly modular base class for LLM interactions.
Supports OpenAI and Google Gemini APIs via environment variables.
"""

import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("LLMBase")

class LLMBase:
    def __init__(self, model_override: Optional[str] = None):
        """
        Dynamically selects the API based on available environment variables.
        Prefers OpenAI if OPENAI_API_KEY is present, otherwise falls back to Gemini.
        """
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
            
        self.openai_key = os.environ.get("OPENAI_API_KEY")
        self.gemini_key = os.environ.get("GEMINI_API_KEY")
        self.ollama_key = os.environ.get("OLLAMA_API_KEY")
        self.model_override = model_override
        
        if self.openai_key:
            self.provider = "openai"
            self.model = self.model_override or "gpt-4o"
            import openai
            self.client = openai.OpenAI(api_key=self.openai_key)
        elif self.gemini_key:
            self.provider = "gemini"
            self.model = self.model_override or "gemini-1.5-pro"
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_key)
            self.client = genai.GenerativeModel(self.model)
        elif self.ollama_key:
            self.provider = "ollama"
            self.model = self.model_override or "llama3"
            import openai
            # Often, cloud hosted Ollama (or OpenAI compatible Ollama endpoints) use the OpenAI client
            # with a custom base_url. If a host isn't provided, we default to localhost or let the user override.
            self.ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434/v1")
            self.client = openai.OpenAI(api_key=self.ollama_key, base_url=self.ollama_host)
        else:
            logger.warning("No OPENAI_API_KEY, GEMINI_API_KEY, or OLLAMA_API_KEY found in environment. LLM calls will fail.")
            self.provider = "none"

    def prompt(self, system_prompt: str, user_prompt: str, response_format: str = "text") -> str:
        """
        Sends a prompt to the LLM and returns the raw string response.
        If response_format="json_object", attempts to force JSON output.
        """
        if self.provider == "none":
            raise ValueError("No LLM API keys configured.")
            
        try:
            if self.provider in ["openai", "ollama"]:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                kwargs = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.2
                }
                if response_format == "json_object":
                    # Some Ollama providers support this native JSON mode
                    kwargs["response_format"] = { "type": "json_object" }
                    
                response = self.client.chat.completions.create(**kwargs)
                return response.choices[0].message.content

            elif self.provider == "gemini":
                # Gemini doesn't strictly separate system/user in the simple generate_content API, 
                # so we combine them cleanly.
                combined_prompt = f"System Instructions:\n{system_prompt}\n\nUser Input:\n{user_prompt}"
                if response_format == "json_object":
                    combined_prompt += "\n\nCRITICAL: You must return a raw valid JSON object. No markdown blocks."
                
                response = self.client.generate_content(
                    combined_prompt,
                    generation_config={"temperature": 0.2}
                )
                return response.text

        except Exception as e:
            logger.error(f"LLM API Call failed: {e}")
            raise e

    def prompt_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Convenience method that guarantees a parsed JSON dictionary."""
        raw_response = self.prompt(system_prompt, user_prompt, response_format="json_object")
        try:
            # Clean up markdown formatting if the LLM leaked backticks
            raw_response = raw_response.strip()
            if raw_response.startswith("```json"):
                raw_response = raw_response[7:-3].strip()
            elif raw_response.startswith("```"):
                raw_response = raw_response[3:-3].strip()
                
            return json.loads(raw_response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON output: {raw_response}")
            raise e
