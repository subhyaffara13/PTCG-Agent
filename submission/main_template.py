import json
import logging
import os
import sys
import datetime
from pathlib import Path

# Setup basic log capture
logger = logging.getLogger(__name__)

# Add agent directory to sys.path to ensure imports find cb_agents and router
agent_dir = str(Path(__file__).parent.resolve()) if "__file__" in globals() and globals()["__file__"] else os.getcwd()
if agent_dir not in sys.path:
    sys.path.insert(0, agent_dir)


# Try to import Orchestrator from cb_agents if not already present
if globals().get("orchestrator") is None:
    try:
        from cb_agents.orchestrator import Orchestrator
        orchestrator = Orchestrator(
            skills_dir=os.path.join(agent_dir, "skills"),
            log_dir=os.path.join(agent_dir, "logs")
        )
        orchestrator.start_game()
    except Exception as global_err:
        logger.error(f"Global orchestrator initialization failed: {global_err}")
        orchestrator = None

# Default deck from the competition environment if not already defined (single-file mode)
_existing_deck = globals().get("DEFAULT_DECK")
if not isinstance(_existing_deck, list) or len(_existing_deck) != 60:
    DEFAULT_DECK = [
        3, 3, 3, 3, 3, 3, 3, 5, 6, 6,
        11, 19, 19, 65, 66, 304, 305, 676, 676, 676,
        676, 677, 678, 722, 723, 741, 742, 743, 878, 879,
        1079, 1081, 1086, 1086, 1086, 1086, 1102, 1115, 1121, 1122,
        1141, 1142, 1145, 1152, 1152, 1152, 1152, 1171, 1182, 1182,
        1182, 1192, 1219, 1225, 1227, 1227, 1227, 1227, 1231, 1255
    ]

    try:
        _deck_csv_path = None
        if "__file__" in globals() and globals()["__file__"]:
            _deck_csv_path = Path(__file__).parent / "deck.csv"
        if not _deck_csv_path or not _deck_csv_path.exists():
            _deck_csv_path = Path("deck.csv")
        if not _deck_csv_path.exists():
            _deck_csv_path = Path("submission/deck.csv")
        
        if _deck_csv_path.exists():
            import csv
            _loaded_deck = []
            with open(_deck_csv_path, "r", encoding="utf-8") as _f:
                _reader = csv.DictReader(_f)
                for _row in _reader:
                    _loaded_deck.extend([int(_row["card_id"])] * int(_row["count"]))
            if len(_loaded_deck) == 60:
                DEFAULT_DECK = _loaded_deck
    except Exception:
        pass



from typing import Any

def get_val(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    try:
        return getattr(obj, key, default)
    except Exception:
        return default

def agent(observation, configuration=None):
    """
    Main Actuation Agent loop parsed by Kaggle Match runtimes.
    """
    # Safe defaults
    DEFAULT_DECK_FALLBACK = [
        3, 3, 3, 3, 3, 3, 3, 5, 6, 6,
        11, 19, 19, 65, 66, 304, 305, 676, 676, 676,
        676, 677, 678, 722, 723, 741, 742, 743, 878, 879,
        1079, 1081, 1086, 1086, 1086, 1086, 1102, 1115, 1121, 1122,
        1141, 1142, 1145, 1152, 1152, 1152, 1152, 1171, 1182, 1182,
        1182, 1192, 1219, 1225, 1227, 1227, 1227, 1227, 1231, 1255
    ]
    fallback_action = [0]
    
    try:
        if observation is None:
            return DEFAULT_DECK_FALLBACK
            
        legal_actions = get_val(observation, "legal_actions")
        select = get_val(observation, "select")
        
        # Check if legacy mock unit test is running
        if legal_actions and select is None:
            return [legal_actions[0]]

        # Step 0: If select is None, we must submit the deck (list of 60 integers) at step 0, and [] otherwise
        if select is None:
            if get_val(observation, "step", 0) == 0:
                # Try to return the global DEFAULT_DECK if it is loaded, otherwise fallback
                try:
                    if "DEFAULT_DECK" in globals() and len(globals()["DEFAULT_DECK"]) == 60:
                        return globals()["DEFAULT_DECK"]
                except Exception:
                    pass
                return DEFAULT_DECK_FALLBACK
            return []

        options = get_val(select, "option", [])
        max_count = get_val(select, "maxCount", 1)
        fallback_action = list(range(min(max_count, len(options)))) if options else [0]

        if "orchestrator" not in globals() or globals()["orchestrator"] is None:
            return fallback_action

        orch = globals()["orchestrator"]

        current = get_val(observation, "current")
        if not current:
            return fallback_action

        # Parse active player state
        my_idx = get_val(current, "yourIndex", 0)
        players = get_val(current, "players", [])
        if len(players) <= my_idx:
            return fallback_action

        my_state = players[my_idx]
        opp_state = players[1 - my_idx] if len(players) > 1 else {}

        # Safely convert CABT board state to simplified game_state dict expected by Orchestrator
        game_state = {
            "my_hand": [get_val(c, "id") for c in get_val(my_state, "hand", []) if c and get_val(c, "id") is not None] if get_val(my_state, "hand") else [],
            "my_deck_count": get_val(my_state, "deckCount", 60),
            "my_prizes": len(get_val(my_state, "prize", [])) if isinstance(get_val(my_state, "prize"), list) else 6,
            "my_active_pokemon": get_val(my_state, "active", [None])[0] if get_val(my_state, "active") else None,
            "my_bench": get_val(my_state, "bench", []),
            
            "opponent_active": get_val(opp_state, "active", [None])[0] if get_val(opp_state, "active") else None,
            "opponent_bench_count": len(get_val(opp_state, "bench", [])) if get_val(opp_state, "bench") else 0,
            "opponent_prizes": len(get_val(opp_state, "prize", [])) if isinstance(get_val(opp_state, "prize"), list) else 6,
            "opponent_discard": get_val(opp_state, "discard", []),
            "opponent_revealed": [],
            "opponent_last_play": None,
            
            "turn_number": get_val(current, "turn", 1),
            "my_active_hp": 100,
            "opponent_active_hp": 100,
            "bench_has_attacker": False
        }

        # Parse legal candidates from options
        game_state["legal_attacks"] = [get_val(opt, "name", "") for opt in options if get_val(opt, "type") == 13]
        game_state["legal_attachments"] = [get_val(opt, "name", "") for opt in options if get_val(opt, "type") == 9]
        game_state["legal_bench"] = [get_val(opt, "name", "") for opt in options if get_val(opt, "type") == 8]
        game_state["legal_evolutions"] = []
        game_state["legal_trainers"] = [get_val(opt, "name", "") for opt in options if get_val(opt, "type") == 7]

        # Parse detailed active HP if present
        my_active = get_val(my_state, "active")
        if my_active and isinstance(my_active, list) and len(my_active) > 0:
            active_pokemon = my_active[0]
            if active_pokemon:
                game_state["my_active_hp"] = get_val(active_pokemon, "hp", 100)

        opp_active = get_val(opp_state, "active")
        if opp_active and isinstance(opp_active, list) and len(opp_active) > 0:
            active_pokemon = opp_active[0]
            if active_pokemon:
                game_state["opponent_active_hp"] = get_val(active_pokemon, "hp", 100)

        # Check if we are at the Main Turn Menu (SelectType 0, Context 0)
        sel_type = get_val(select, "type")
        sel_ctx = get_val(select, "context")

        if sel_type == 0 and sel_ctx == 0:
            # Call orchestrator to determine action strategy string
            decision = orch.run_turn(game_state)
            action_label = (decision.primary_action.lower() 
                            if hasattr(decision, "primary_action") 
                            else str(decision).lower())

            # Map orchestrator's prefix action labels to actual select options
            mapped_indices = []
            if action_label.startswith("attack:"):
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") == 13]
            elif action_label.startswith("attach_energy:"):
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") == 9]
            elif action_label.startswith("bench:") or action_label.startswith("evolve:"):
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") == 8]
            elif action_label.startswith("play_trainer:"):
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") == 7]
            elif action_label.startswith("retreat:"):
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") == 10]

            # If no matches, or action is PASS, look for pass/done (Type 14)
            if not mapped_indices or action_label == "pass":
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") == 14]

            # If still nothing, fallback to first index
            if not mapped_indices:
                mapped_indices = [0]

            # Fill selected indices up to max_count
            selected = []
            for idx in (mapped_indices + list(range(len(options)))):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
            return selected
        else:
            # Non-main choice (e.g. starting setup, coin flips, Yes/No, card selection from deck)
            # Use safe fallback (select first N options)
            return fallback_action

    except Exception as e:
        import sys
        sys.stderr.write(f"Agent execution crashed internally: {e}\n")
        try:
            _log_action_exception(e)
        except Exception:
            pass
        
        # Determine whether to return fallback deck or fallback action
        try:
            if observation is None or get_val(observation, "select") is None:
                if "DEFAULT_DECK" in globals() and len(globals()["DEFAULT_DECK"]) == 60:
                    return globals()["DEFAULT_DECK"]
                return DEFAULT_DECK_FALLBACK
        except Exception:
            pass
        return fallback_action

def _log_action_exception(exc: Exception):
    try:
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "action_log.json"
        
        error_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event": "submission_agent_crash",
            "agent_called": "submission/main.py",
            "packet_type": "exception",
            "error_reason": str(exc)
        }
        
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
        pass
