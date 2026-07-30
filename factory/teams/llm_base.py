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
        
        self.provider = "none"
        self.client = None
        self.model = None
        
        self.siliconflow_key = os.environ.get("SILICONFLOW_API_KEY")
        
        if self.openai_key:
            try:
                import openai
                self.provider = "openai"
                self.model = self.model_override or os.environ.get("OPENAI_MODEL", "gpt-4o")
                base_url = os.environ.get("OPENAI_API_BASE") or os.environ.get("OPENAI_BASE_URL")
                self.client = openai.OpenAI(api_key=self.openai_key, base_url=base_url)
            except ImportError:
                logger.warning("OpenAI key found but 'openai' module is missing. Falling back...")

        if self.provider == "none" and self.siliconflow_key:
            try:
                import openai
                self.provider = "openai"
                self.model = self.model_override or os.environ.get("SILICONFLOW_MODEL", "Qwen/Qwen2.5-72B-Instruct")
                self.client = openai.OpenAI(api_key=self.siliconflow_key, base_url="https://api.siliconflow.cn/v1")
            except ImportError:
                logger.warning("SiliconFlow key found but 'openai' module is missing. Falling back...")

        if self.provider == "none" and self.gemini_key:
            try:
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=FutureWarning)
                    import google.generativeai as genai  # type: ignore
                self.provider = "gemini"
                self.model = self.model_override or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
                genai.configure(api_key=self.gemini_key)
                self.client = genai
            except ImportError:
                logger.warning("Gemini key found but 'google.generativeai' module is missing. Falling back...")

        if self.provider == "none" and self.ollama_key:
            try:
                import openai
                # Auto-detect SiliconFlow API key formats configured as OLLAMA_API_KEY
                if len(self.ollama_key) == 57 and "." in self.ollama_key:
                    self.provider = "openai"
                    self.model = self.model_override or os.environ.get("OLLAMA_MODEL") or os.environ.get("SILICONFLOW_MODEL", "Qwen/Qwen2.5-72B-Instruct")
                    self.client = openai.OpenAI(api_key=self.ollama_key, base_url="https://api.siliconflow.cn/v1")
                    logger.info(f"Auto-routed OLLAMA_API_KEY as SiliconFlow provider with model {self.model}")
                else:
                    self.provider = "ollama"
                    self.model = self.model_override or os.environ.get("OLLAMA_MODEL", "llama3")
                    self.ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434/v1")
                    self.client = openai.OpenAI(api_key=self.ollama_key, base_url=self.ollama_host)
            except ImportError:
                logger.warning("Ollama key found but 'openai' module is missing. Cannot use Ollama.")

        if self.provider == "none":
            logger.warning("No valid OPENAI, GEMINI, or OLLAMA configuration found or dependencies missing. LLM calls will fail.")

    def prompt(self, system_prompt: str, user_prompt: str, response_format: str = "text") -> str:
        """
        Sends a prompt to the LLM and returns the raw string response.
        If response_format="json_object", attempts to force JSON output.
        """
        if self.provider == "none" or self.client is None:
            raise ValueError("No LLM API keys configured.")
            
        try:
            if self.provider in ["openai", "ollama"]:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                kwargs: Dict[str, Any] = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.2
                }
                if response_format == "json_object":
                    kwargs["response_format"] = { "type": "json_object" }
                    
                response = self.client.chat.completions.create(**kwargs)
                return response.choices[0].message.content or ""

            elif self.provider == "gemini":
                combined_prompt = f"System Instructions:\n{system_prompt}\n\nUser Input:\n{user_prompt}"
                if response_format == "json_object":
                    combined_prompt += "\n\nCRITICAL: You must return a raw valid JSON object. No markdown blocks."
                
                model_obj = self.client.GenerativeModel(self.model)
                response = model_obj.generate_content(combined_prompt)
                return response.text or ""
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")

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
