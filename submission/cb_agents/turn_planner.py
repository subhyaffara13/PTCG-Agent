"""
agents/turn_planner.py

Evaluates the priority rules matching the active hand profile, filters legal actions
against game_state limits, sorts sequences, and outputs action_sequence layouts.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List
from cb_agents.base_agent import BaseAgent
from router.bus import TurnPlannerPacket

logger = logging.getLogger(__name__)

class TurnPlanner(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "player", shared_context=None):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.shared_context = shared_context
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        # Load priority rules on init only
        if self.shared_context:
            self.rules = self.shared_context.get_config(str(self.skills_dir), "priority_rules.json")
        else:
            self.rules = self._load_priority_rules()
            
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"

    def _load_priority_rules(self) -> dict:
        path = self.skills_dir / "priority_rules.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to read priority_rules.json: {e}")
        return {"rules": []}

    def receive(self, packet: Any) -> dict:
        """
        Accepts and processes TurnPlannerPacket. Returns action sequences.
        """
        # Type check validation
        if not isinstance(packet, TurnPlannerPacket):
            raise TypeError(
                f"TurnPlanner received an illegal packet type: {type(packet).__name__}."
            )

        hand_score = packet.hand_score
        priority_profile = packet.priority_profile
        top_play = packet.top_play
        game_state = getattr(packet, "game_state", {}) or {}
        turn = getattr(packet, "turn", 1)

        # Default profile check
        valid_profiles = {"aggro_push", "setup", "disruption", "stall", "closing"}
        if priority_profile not in valid_profiles:
            priority_profile = "aggro_push"

        # STEP 1: Build and validate legal candidate actions against game_state
        candidates = self._build_legal_candidates(game_state)

        # STEP 2: Sort candidates according to active profile priorities
        sorted_actions = self._sort_actions(candidates, priority_profile, game_state)

        # Always guarantee at least ["pass"] exists
        if not sorted_actions:
            sorted_actions = ["pass"]

        primary_action = sorted_actions[0]

        # STEP 3: Build reasoning chain
        reasoning_chain = f"Profile {priority_profile}, primary action {primary_action} because evaluated priority match."

        response = {
            "action_sequence": sorted_actions,
            "primary_action": primary_action,
            "reasoning_chain": reasoning_chain
        }

        # Log reasoning
        self._log_reasoning(turn, priority_profile, response)
        return response

    def _build_legal_candidates(self, game_state: dict) -> List[str]:
        """
        Extracts legal moves matching the action formats:
        - "attack:{move_name}"
        - "evolve:{card_name}"
        - "attach_energy:{target_pokemon}"
        - "play_trainer:{card_name}"
        - "bench:{card_name}"
        - "pass"
        """
        # Read from game_state keys, falling back to basic mock moves if empty
        candidates = []
        
        legal_attacks = game_state.get("legal_attacks", [])
        for attack in legal_attacks:
            candidates.append(f"attack:{attack}")
            
        legal_evolutions = game_state.get("legal_evolutions", [])
        for evo in legal_evolutions:
            candidates.append(f"evolve:{evo}")
            
        legal_attachments = game_state.get("legal_attachments", [])
        for target in legal_attachments:
            candidates.append(f"attach_energy:{target}")
            
        legal_trainers = game_state.get("legal_trainers", [])
        for trainer in legal_trainers:
            candidates.append(f"play_trainer:{trainer}")
            
        legal_bench = game_state.get("legal_bench", [])
        for basic in legal_bench:
            candidates.append(f"bench:{basic}")

        candidates.append("pass")
        return candidates

    def _sort_actions(self, candidates: List[str], profile: str, game_state: dict) -> List[str]:
        """Sorts actions based on the explicit priority order per profile."""
        
        # Profile order registries: non-ending moves first, then attack, then pass
        profile_orders = {
            "aggro_push": ["evolve:", "attach_energy:", "play_trainer:", "bench:", "attack:", "pass"],
            "setup": ["bench:", "play_trainer:", "attach_energy:", "evolve:", "attack:", "pass"],
            "disruption": ["play_trainer:", "bench:", "attach_energy:", "evolve:", "attack:", "pass"],
            "stall": ["play_trainer:", "bench:", "attach_energy:", "evolve:", "attack:", "pass"],
            "closing": ["attach_energy:", "attack:", "evolve:", "play_trainer:", "bench:", "pass"]
        }

        order = profile_orders.get(profile, profile_orders["aggro_push"])

        active_pokemon = game_state.get("my_active_pokemon")
        over_attached = False
        if isinstance(active_pokemon, dict):
            card_id = active_pokemon.get("id")
            attached_count = len(active_pokemon.get("energies", []))
            needed = 3 if card_id == 722 else 2
            if attached_count >= needed:
                over_attached = True

        def get_priority_rank(action: str) -> tuple:
            cat_rank = len(order)
            for rank, prefix in enumerate(order):
                if action.startswith(prefix):
                    cat_rank = rank
                    break

            micro_rank = 0
            if action.startswith("play_trainer:"):
                trainer_name = action.split(":", 1)[1]
                if "Research" in trainer_name or "Professor" in trainer_name:
                    micro_rank = -2
                elif "Ball" in trainer_name:
                    micro_rank = 2
            elif action.startswith("attach_energy:"):
                if over_attached:
                    cat_rank = order.index("pass") - 1
                    micro_rank = 10

            return (cat_rank, micro_rank, action)

        return sorted(candidates, key=get_priority_rank)

    def _log_reasoning(self, turn: int, profile: str, response: dict):
        log_entry = {
            "turn": turn,
            "priority_profile": profile,
            "action_sequence": response["action_sequence"],
            "primary_action": response["primary_action"],
            "reasoning_chain": response["reasoning_chain"]
        }
        try:
            logs = []
            if self.reasoning_log_file.exists():
                content = self.reasoning_log_file.read_text(encoding="utf-8").strip()
                if content:
                    try:
                        logs = json.loads(content)
                        if not isinstance(logs, list):
                            logs = [logs]
                    except json.JSONDecodeError:
                        logs = []
            logs.append(log_entry)
            self.reasoning_log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to log turn planner decision: {e}")
