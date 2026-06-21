"""
agents/orchestrator_state.py
State helper utilities for Orchestrator.
"""
import json
from pathlib import Path
from typing import Dict, Any
from agents.registry import get_registered_agents

def load_delegation_map(skills_dir: Path) -> dict:
    path = skills_dir / "delegation_map.json"
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data.get("delegation", {})
        except:
            pass
    return {
        "turn_start": "hand_analyst",
        "after_hand_analysis": "turn_planner",
        "on_trigger": "strategy_agent",
        "on_opponent_play": "opponent_model",
        "before_turn_planner": "lethal_calculator",
        "always": "time_manager"
    }

def initialize_and_register_agents(orchestrator: Any):
    """Initializes and registers sub-agents on the bus."""
    for bus_name, meta in get_registered_agents().items():
        kwargs: dict = {"log_dir": str(orchestrator.log_dir)}
        if meta["needs_skills_dir"]:
            kwargs["skills_dir"] = str(orchestrator.skills_dir)
        if meta["needs_shared_context"]:
            kwargs["shared_context"] = orchestrator.context

        instance = meta["cls"](**kwargs)
        setattr(orchestrator, bus_name, instance)

        reg_kwargs: dict = {}
        if meta["perspective_flag"] != "player":
            reg_kwargs["perspective_flag"] = meta["perspective_flag"]
        orchestrator.bus.register_agent(bus_name, instance.receive, **reg_kwargs)
