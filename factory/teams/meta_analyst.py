"""
factory/teams/meta_analyst.py

Analyzes match logs and replay data to extract actionable anti-patterns using the LLM.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List
from factory.teams.llm_base import LLMBase

logger = logging.getLogger("MetaAnalyst")

class MetaAnalyst(LLMBase):
    def __init__(self, model_override=None):
        super().__init__(model_override)
        
    def analyze_logs(self, log_directory: str = "logs") -> List[Dict[str, Any]]:
        """
        Reads recent match reports, learned rules, and uses the LLM to deduce anti-patterns.
        """
        logger.info("MetaAnalyst analyzing match logs...")
        
        bandit_report_path = Path("bandit_report.json")
        report_data = "{}"
        if bandit_report_path.exists():
            report_data = bandit_report_path.read_text(encoding="utf-8")
            
        # Read learned don'ts and do's
        donts_path = Path("skills/learned_donts.json")
        dos_path = Path("skills/learned_dos.json")
        donts_data = "{}"
        dos_data = "{}"
        if donts_path.exists():
            donts_data = donts_path.read_text(encoding="utf-8")
        if dos_path.exists():
            dos_data = dos_path.read_text(encoding="utf-8")
        
        system_prompt = (
            "You are an expert Data Scientist specializing in Pokémon TCG AlphaZero agents. "
            "Your job is to read raw match logs and output a strict JSON list of strategic 'anti-patterns' "
            "where the agent played suboptimally. Return ONLY a JSON list of objects, where each object has: "
            "'issue_name' (string) and 'description' (string)."
        )
        
        user_prompt = (
            f"Here is the recent match data:\n\n{report_data}\n\n"
            f"Here are the recently extracted negative play anti-patterns (learned_donts):\n\n{donts_data}\n\n"
            f"Here are the positive play patterns (learned_dos):\n\n{dos_data}\n\n"
            "Identify the top 3 anti-patterns."
        )
        
        try:
            results = self.prompt_json(system_prompt, user_prompt)
            # Ensure it's a list
            if isinstance(results, dict) and "anti_patterns" in results:
                return results["anti_patterns"]
            elif isinstance(results, list):
                return results
            else:
                return [{"issue_name": "Parsing Error", "description": "LLM did not return a list."}]
        except Exception as e:
            logger.error(f"MetaAnalyst failed: {e}")
            return []
