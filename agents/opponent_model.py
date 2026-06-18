"""
agents/opponent_model.py

Opponent modelling sub-agent.
Infers opponent's hidden state from revealed information only.
Predicts opponent's next action to inform strategy decisions.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict
from agents.base_agent import BaseAgent
from router.bus import OpponentModelPacket

logger = logging.getLogger(__name__)

class OpponentModel(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "opponent"):
        # PERSPECTIVE_FLAG = "opponent" always
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        # Load once on init only
        self.archetypes = self._load_deck_archetypes()
        self.revealed_state = []  # cards opponent has played
        self.inferred_state = {}  # probabilistic fill
        self.archetype_confidence = 0.0
        self.identified_archetype = "unknown"

    def _load_deck_archetypes(self) -> dict:
        path = self.skills_dir / "deck_archetypes.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                return data.get("archetypes", {})
            except Exception as e:
                logger.error(f"Failed to read deck_archetypes.json: {e}")
        return {}

    def receive(self, packet: Any) -> dict:
        """
        Accepts and processes OpponentModelPacket.
        """
        if not isinstance(packet, OpponentModelPacket):
            raise TypeError(
                f"OpponentModel received an illegal packet type: {type(packet).__name__}."
            )

        revealed_cards = getattr(packet, "revealed_cards", []) or getattr(packet, "newly_played_cards", [])
        turn_number = getattr(packet, "turn_number", 1) or getattr(packet, "turn", 1)
        active_pokemon = getattr(packet, "active_pokemon", None) or getattr(packet, "revealed_active_pokemon", None)
        prizes_remaining = getattr(packet, "prizes_remaining", 6) or getattr(packet, "revealed_prizes_remaining", 6)
        discard_pile = getattr(packet, "discard_pile", []) or getattr(packet, "revealed_discard", [])

        # STEP 1: Update revealed_state
        for card in revealed_cards:
            if card not in self.revealed_state:
                self.revealed_state.append(card)

        # STEP 2: Update archetype_confidence
        # Compare revealed_state against each archetype in deck_archetypes.json
        total_revealed = len(self.revealed_state)
        
        if total_revealed < 3 or not self.archetypes:
            # Minimum 3 revealed cards before confidence > 0.0
            self.archetype_confidence = 0.0
            self.identified_archetype = "unknown"
        else:
            best_match_count = 0
            best_archetype = "unknown"
            
            for arch_name, arch_data in self.archetypes.items():
                signature_cards = set(arch_data.get("signature_cards", []))
                card_pool = set(arch_data.get("card_pool", []))
                
                # Count matches
                matches = sum(1 for c in self.revealed_state if c in signature_cards or c in card_pool)
                if matches > best_match_count:
                    best_match_count = matches
                    best_archetype = arch_name
            
            if best_match_count > 0:
                self.archetype_confidence = round(best_match_count / total_revealed, 4)
                self.identified_archetype = best_archetype
            else:
                self.archetype_confidence = 0.0
                self.identified_archetype = "unknown"

        # STEP 3: Fill inferred_state
        # For identified_archetype load its card pool, exclude already revealed
        if self.identified_archetype != "unknown" and self.identified_archetype in self.archetypes:
            pool = self.archetypes[self.identified_archetype].get("card_pool", [])
            self.inferred_state = {c: 1.0 for c in pool if c not in self.revealed_state}
        else:
            self.inferred_state = {}

        # STEP 4: Predict next action
        predicted = "unknown"
        if self.identified_archetype == "aggro":
            # Estimate energy attached by inspecting discard or board (assume attached if we have prizes mismatch)
            if prizes_remaining < 6:
                predicted = "attack"
            else:
                predicted = "attach_energy"
        elif self.identified_archetype == "control":
            if prizes_remaining <= 3:
                predicted = "play_trainer_disruption"
            else:
                predicted = "stall"
        elif self.identified_archetype == "combo":
            if turn_number < 3:
                predicted = "setup_bench"
            else:
                predicted = "execute_combo"
        else:
            predicted = "unknown"

        # STEP 5: Build reasoning
        reasoning = f"Identified {self.identified_archetype} with {round(self.archetype_confidence * 100, 2)}% confidence based on {total_revealed} revealed cards. Predicting {predicted}."

        return {
            "predicted_next_action": predicted,
            "archetype_confidence": self.archetype_confidence,
            "inferred_deck_type": self.identified_archetype,
            "reasoning": reasoning
        }
