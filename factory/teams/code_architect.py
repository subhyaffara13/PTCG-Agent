"""
factory/teams/code_architect.py

Uses the LLM to propose concrete code modifications based on anti-patterns.
"""

import logging
from typing import Dict, Any, List
from factory.teams.llm_base import LLMBase

logger = logging.getLogger("CodeArchitect")

class CodeArchitect(LLMBase):
    def __init__(self, model_override=None):
        super().__init__(model_override)
        
    def propose_code_fixes(self, anti_patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Takes a list of anti-patterns and asks the LLM to write code diffs or heuristic logic.
        """
        if not anti_patterns:
            logger.info("No anti-patterns found. Skipping code architecture.")
            return {}
            
        logger.info(f"CodeArchitect analyzing {len(anti_patterns)} anti-patterns...")
        
        system_prompt = (
            "You are a Principal C++/Python Software Engineer. "
            "You are given strategic flaws in a Pokémon TCG AlphaZero agent. "
            "Your job is to propose EXACT code edits to fix these issues. "
            "Return a JSON object containing a 'files_to_edit' list, where each object has: "
            "'filepath', 'original_code', 'new_code', and 'reasoning'."
        )
        
        user_prompt = f"Here are the anti-patterns currently plaguing the agent:\n\n{anti_patterns}\n\nPlease generate the required C++ or Python heuristic edits."
        
        try:
            results = self.prompt_json(system_prompt, user_prompt)
            return results
        except Exception as e:
            logger.error(f"CodeArchitect failed: {e}")
            return {}
