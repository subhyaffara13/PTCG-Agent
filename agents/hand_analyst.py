"""
agents/hand_analyst.py

Scores the player's opening or active hand composition, determines current strategy
profile priorities, selects the top card option, and logs reasoning.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List
from agents.base_agent import BaseAgent
from router.bus import HandAnalystPacket

logger = logging.getLogger(__name__)

class HandAnalyst(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "player"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        # Load card pool scoring data on init only
        self.card_pool = self._load_card_pool()
        self.card_lookup = {c["card_id"]: c for c in self.card_pool}
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"

    def _load_card_pool(self) -> list:
        path = self.skills_dir / "card_scoring.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                return data.get("cards", [])
            except Exception as e:
                logger.error(f"Failed to read card_scoring.json: {e}")
        return []

    def receive(self, packet: Any) -> dict:
        """
        Accepts and processes HandAnalystPacket. Returns scoring profiles.
        """
        # Type check constraint
        if not isinstance(packet, HandAnalystPacket):
            raise TypeError(
                f"HandAnalyst received an illegal packet type: {type(packet).__name__}."
            )

        hand = packet.hand
        deck_remaining = packet.deck_remaining
        turn = getattr(packet, "turn", 1)
        opponent_prizes = getattr(packet, "opponent_prizes_remaining", 6)

        # Empty hand fallback check
        if not hand:
            response = {
                "hand_score": 0.0,
                "priority_profile": "stall",
                "top_play": "none",
                "reasoning_chain": "Empty hand — stall profile activated"
            }
            self._log_reasoning(turn, response)
            return response

        # STEP 1: Score cards
        ev_scores = []
        has_basic = False
        has_supporter = False
        has_energy = False
        hand_cards_data = []

        for cid in hand:
            card = self.card_lookup.get(cid)
            if card:
                ev_score = card.get("ev_score", 0.1)
                ctype = card.get("card_type", "Trainer")
                tags = card.get("combo_tags", [])
                
                if ctype == "Pokemon" and "Basic" in tags:
                    has_basic = True
                elif ctype == "Trainer" and "Supporter" in tags:
                    has_supporter = True
                elif ctype == "Energy":
                    has_energy = True
                
                hand_cards_data.append((card, ev_score))
            else:
                ev_score = 0.1
                hand_cards_data.append(({"card_id": cid, "card_name": cid, "card_type": "Trainer"}, ev_score))
            ev_scores.append(ev_score)

        # STEP 2: Calculate hand_score
        avg_ev = sum(ev_scores) / len(ev_scores)
        bonus = 0.0
        if has_basic:
            bonus += 0.1
        if has_supporter:
            bonus += 0.1
        if has_energy:
            bonus += 0.1
        
        hand_score = min(1.0, avg_ev + bonus)

        # STEP 3: Priority profile selection logic
        has_attacker = any(c[0].get("damage_output", 0) > 0 for c in hand_cards_data if c[0].get("card_type") == "Pokemon")
        has_evolution = any(c[0].get("card_type") == "Pokemon" and "Stage" in c[0].get("card_name", "") for c in hand_cards_data)
        control_count = sum(1 for c in hand_cards_data if c[0].get("archetype") == "control")

        if has_attacker and has_energy and hand_score > 0.5:
            priority_profile = "aggro_push"
        elif (has_basic and not has_energy) or (has_evolution and not has_basic) or hand_score < 0.3:
            priority_profile = "setup"
        elif control_count >= 2 and opponent_prizes <= 3:
            priority_profile = "disruption"
        elif deck_remaining < 10 or (not has_attacker and not has_supporter):
            priority_profile = "stall"
        else:
            priority_profile = "aggro_push"

        # STEP 4: Identify top play
        # Highest ev_score, resolve tie using Pokemon > Trainer > Energy
        def sort_key(item):
            card, ev = item
            ctype = card.get("card_type", "Trainer")
            if ctype == "Pokemon":
                type_priority = 3
            elif ctype == "Trainer":
                type_priority = 2
            else:
                type_priority = 1
            return (ev, type_priority)

        hand_cards_data.sort(key=sort_key, reverse=True)
        top_play_card = hand_cards_data[0][0]
        top_play = top_play_card.get("card_name", top_play_card.get("card_id", "none"))

        # STEP 5: Build reasoning chain
        reasoning_chain = f"Hand score {round(hand_score, 4)}, profile {priority_profile} because composition metrics resolved state check."

        response = {
            "hand_score": round(hand_score, 4),
            "priority_profile": priority_profile,
            "top_play": top_play,
            "reasoning_chain": reasoning_chain
        }

        # Log reasoning details
        self._log_reasoning(turn, response)
        return response

    def _log_reasoning(self, turn: int, response: dict):
        log_entry = {
            "turn": turn,
            "hand_score": response["hand_score"],
            "priority_profile": response["priority_profile"],
            "top_play": response["top_play"],
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
            logger.error(f"Failed to write logic logs: {e}")
