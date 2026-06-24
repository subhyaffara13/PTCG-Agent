"""
agents/hand_analyst.py
Analyzes hand contents and computes prized probabilities.
"""
from pathlib import Path
from typing import Any
from cb_agents.base_agent import BaseAgent
from cb_agents.card_registry import CardRegistry
from cb_agents.registry import register_agent
from cb_agents.logging_helper import append_and_flush_logs
from cb_agents.deck_loader import load_deck_base_list, load_hand_analyst_configs

@register_agent("hand_analyst")
class HandAnalyst(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "player", shared_context=None):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        self.registry = CardRegistry(self.skills_dir)
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"
        self.prize_mapper_file = self.log_dir / "prize_mapper_reasoning.json"
        self._reasoning_buffer = []
        self._prize_mapper_buffer = []
        self.deck_base_list = load_deck_base_list(self.skills_dir)
        self.shared_context = shared_context
        load_hand_analyst_configs(self, shared_context)

    def receive(self, packet: Any) -> dict:
        from cb_agents.hand_analyst_run import run_hand_analyst
        return run_hand_analyst(self, packet)

    def _log_reasoning(self, turn: int, response: dict):
        self._reasoning_buffer.append({
            "turn": turn,
            "hand_score": response["hand_score"],
            "priority_profile": response["priority_profile"],
            "top_play": response["top_play"],
            "reasoning_chain": response["reasoning_chain"]
        })

    def flush_logs(self):
        append_and_flush_logs(self.reasoning_log_file, self._reasoning_buffer)
        append_and_flush_logs(self.prize_mapper_file, self._prize_mapper_buffer)
