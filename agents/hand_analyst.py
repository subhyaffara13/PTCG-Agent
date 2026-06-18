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
from agents.card_registry import CardRegistry

logger = logging.getLogger(__name__)

class HandAnalyst(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "player", shared_context=None):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.shared_context = shared_context
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        # Load card pool scoring data on init only
        self.registry = CardRegistry(self.skills_dir)
        self.card_lookup = self.registry.cards
        
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"
        self.prize_mapper_file = self.log_dir / "prize_mapper_reasoning.json"
        self._reasoning_buffer = []  # In-memory buffer, NO disk I/O per turn
        self._prize_mapper_buffer = []  # In-memory buffer for prize mapper logs
        self.deck_base_list = self._load_deck_base_list()

    def _load_deck_base_list(self) -> dict:
        # Try finding deck configurations
        path = self.skills_dir.parent / "agents" / "deck_new.csv"
        if not path.exists():
            path = self.skills_dir.parent / "deck.csv"
        if not path.exists():
            path = Path("agents/deck_new.csv")
        if not path.exists():
            path = Path("deck.csv")
            
        deck_dict = {}
        if path.exists():
            try:
                import csv
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            cid = int(row["card_id"])
                            count = int(row["count"])
                            deck_dict[cid] = count
                        except:
                            pass
            except Exception as e:
                logger.error(f"Failed to load deck list in HandAnalyst: {e}")
        return deck_dict


    def _load_card_pool(self) -> list:
        path = self.skills_dir / "card_scoring.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                return data.get("cards", [])
            except Exception as e:
                logger.error(f"Failed to read card_scoring.json: {e}")
        return []

    def _get_phase(self, turn: int) -> str:
        """Returns the game phase based on the current turn number."""
        if turn <= 3:
            return 'early'
        elif turn <= 8:
            return 'mid'
        else:
            return 'late'

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
        
        discard = getattr(packet, "discard", []) or []
        board = getattr(packet, "board", []) or []

        # Prize Zone Mapper Deduction logic
        revealed_counts = {}
        for cid in hand + discard + board:
            try:
                cid_int = int(cid)
                revealed_counts[cid_int] = revealed_counts.get(cid_int, 0) + 1
            except:
                pass
                
        total_revealed_count = sum(revealed_counts.values())
        total_starting_count = sum(self.deck_base_list.values()) if self.deck_base_list else 60
        total_unrevealed = max(0, total_starting_count - total_revealed_count)
        prize_remaining = max(0, total_unrevealed - deck_remaining)
        
        prized_probabilities = {}
        if total_unrevealed > 0 and prize_remaining > 0:
            import math
            def nCr(n, r):
                if r < 0 or r > n:
                    return 0
                return math.comb(n, r)
                
            for cid_int, start_count in self.deck_base_list.items():
                rev_count = revealed_counts.get(cid_int, 0)
                n_unrevealed = max(0, start_count - rev_count)
                if n_unrevealed > 0:
                    prob = 1.0 - (nCr(total_unrevealed - n_unrevealed, prize_remaining) / nCr(total_unrevealed, prize_remaining))
                    prized_probabilities[str(cid_int)] = round(prob, 4)
                else:
                    prized_probabilities[str(cid_int)] = 0.0

        # Log prized mapping
        if prized_probabilities:
            self._prize_mapper_buffer.append({
                "turn": turn,
                "perspective": self.perspective_flag,
                "prize_remaining": prize_remaining,
                "total_unrevealed": total_unrevealed,
                "prized_probabilities": prized_probabilities
            })

        # Empty hand fallback check
        if not hand:
            response = {
                "hand_score": 0.0,
                "priority_profile": "stall",
                "top_play": "none",
                "reasoning_chain": "Empty hand — stall profile activated",
                "prized_probabilities": {}
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
                    ev_score += 0.05  # flat energy-in-hand relevance bonus
                
                hand_cards_data.append((card, ev_score))
            else:
                ev_score = 0.1
                hand_cards_data.append(({"card_id": cid, "card_name": cid, "card_type": "Trainer"}, ev_score))
            ev_scores.append(ev_score)

        # STEP 2: Calculate hand_score with phase-aware bonuses
        phase = self._get_phase(turn)
        avg_ev = sum(ev_scores) / len(ev_scores)
        bonus = 0.0

        if phase == 'early':
            if has_basic:
                bonus += 0.15
            if has_supporter:
                bonus += 0.1
        elif phase == 'mid':
            if has_energy:
                bonus += 0.15
            has_evolution = any(
                c[0].get("card_type") == "Pokemon" and "Stage" in c[0].get("card_name", "")
                for c in hand_cards_data
            )
            if has_evolution:
                bonus += 0.1
        else:  # late
            has_late_attacker = any(
                c[0].get("damage_output", 0) > 0
                for c in hand_cards_data if c[0].get("card_type") == "Pokemon"
            )
            if has_late_attacker:
                bonus += 0.15
            high_ev_count = sum(1 for c in hand_cards_data if c[1] > 0.6)
            if high_ev_count > 0:
                bonus += 0.1

        hand_score = min(1.0, avg_ev + bonus)

        # STEP 3: Priority profile selection logic
        has_attacker = any(c[0].get("damage_output", 0) > 0 for c in hand_cards_data if c[0].get("card_type") == "Pokemon")
        has_evolution = any(c[0].get("card_type") == "Pokemon" and "Stage" in c[0].get("card_name", "") for c in hand_cards_data)
        control_count = sum(1 for c in hand_cards_data if c[0].get("archetype") == "control")

        # Closing profile: maximum aggression when opponent is nearly out
        if opponent_prizes <= 2 and has_attacker:
            priority_profile = "closing"
        elif has_attacker and has_energy and hand_score > 0.35:
            priority_profile = "aggro_push"
        elif (has_basic and not has_energy) or (has_evolution and not has_basic) or hand_score < 0.3:
            priority_profile = "setup"
        elif control_count >= 2 and opponent_prizes <= 3:
            priority_profile = "disruption"
        # PrizeTracker proxy: mathematically unlikely to draw an attacker if deck is thin
        elif deck_remaining < 15 and not has_attacker:
            priority_profile = "stall"
        else:
            # Phase-aware default
            priority_profile = "setup" if phase == 'early' else "aggro_push"

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
            "reasoning_chain": reasoning_chain,
            "prized_probabilities": prized_probabilities if 'prized_probabilities' in locals() else {}
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
        self._reasoning_buffer.append(log_entry)

    def flush_logs(self):
        """Write all buffered logs to disk. Called once at end of game."""
        if self._reasoning_buffer:
            try:
                self.reasoning_log_file.write_text(
                    json.dumps(self._reasoning_buffer, indent=2), encoding='utf-8'
                )
            except Exception as e:
                logger.error(f"Failed to flush reasoning logs: {e}")
            self._reasoning_buffer.clear()
        if self._prize_mapper_buffer:
            prize_log_file = self.log_dir / "prize_mapper_reasoning.json"
            try:
                prize_log_file.write_text(
                    json.dumps(self._prize_mapper_buffer, indent=2), encoding='utf-8'
                )
            except Exception as e:
                logger.error(f"Failed to flush prize mapper logs: {e}")
            self._prize_mapper_buffer.clear()
