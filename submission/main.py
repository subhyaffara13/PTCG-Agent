"""
submission/main.py

Kaggle Competition submission entry point wrapper.
Translates observation and configuration inputs into standardized game_state dictionaries,
dispatches to the Orchestrator, type validates the outcome, and executes fallbacks.
"""

import json
import logging
import os
import sys
from pathlib import Path

# Add parent directory to path to resolve import layers correctly in Kaggle environment
sys.path.append(str(Path(__file__).parent.parent))

from agents.orchestrator import Orchestrator

# Setup basic log capture
logger = logging.getLogger(__name__)

# GLOBAL SETUP (runs once on load)
try:
    orchestrator = Orchestrator()
    orchestrator.start_game()
except Exception as global_err:
    logger.error(f"Global orchestrator initialization failed: {global_err}")
    orchestrator = None

def agent(observation, configuration=None) -> str:
    """
    Main Actuation Agent loop parsed by Kaggle Match runtimes.
    """
    # Safeguard wrapper: never crash, return legal action index
    fallback_action = "pass"
    if hasattr(observation, "legal_actions") and observation.legal_actions:
        fallback_action = observation.legal_actions[0]

    if orchestrator is None:
        return fallback_action

    try:
        # STEP 1: Parse observation safely using getattr fallbacks
        game_state = {
            "my_hand": getattr(observation, "hand", []),
            "my_deck_count": getattr(observation, "deck_count", 60),
            "my_prizes": getattr(observation, "prizes", 6),
            "my_active_pokemon": getattr(observation, "active", None),
            "my_bench": getattr(observation, "bench", []),
            "opponent_active": getattr(observation, "opponent_active", None),
            "opponent_bench_count": getattr(observation, "opponent_bench_count", 0),
            "opponent_prizes": getattr(observation, "opponent_prizes", 6),
            "opponent_discard": getattr(observation, "opponent_discard", []),
            "opponent_revealed": getattr(observation, "opponent_revealed", []),
            "opponent_last_play": getattr(observation, "opponent_last_play", None),
            "turn_number": getattr(observation, "turn", 1),
            
            # Additional board elements required by orchestrator/strategy agent
            "my_active_hp": getattr(observation, "my_active_hp", 100),
            "opponent_active_hp": getattr(observation, "opponent_active_hp", 100),
            "bench_has_attacker": getattr(observation, "bench_has_attacker", False)
        }

        # STEP 2: Call orchestrator
        action = orchestrator.run_turn(game_state)

        # STEP 3: Validate action is legal
        legal_actions = getattr(observation, "legal_actions", [])
        if legal_actions:
            if action not in legal_actions:
                action = legal_actions[0]
        else:
            action = "pass"

        # STEP 4: Return action string
        return action

    except Exception as e:
        # Log to logs/action_log.json if possible
        _log_action_exception(e)
        return fallback_action

def _log_action_exception(exc: Exception):
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "action_log.json"
    
    error_entry = {
        "timestamp": "",
        "event": "submission_agent_crash",
        "agent_called": "submission/main.py",
        "packet_type": "exception",
        "error_reason": str(exc)
    }
    
    try:
        logs = []
        if log_file.exists():
            content = log_file.read_text(encoding="utf-8").strip()
            if content:
                try:
                    logs = json.loads(content)
                    if not isinstance(logs, list):
                        logs = [logs]
                except json.JSONDecodeError:
                    logs = []
        logs.append(error_entry)
        log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
    except Exception as log_err:
        logger.error(f"Failed to log crash event to {log_file}: {log_err}")
