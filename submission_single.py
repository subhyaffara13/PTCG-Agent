# Single-file self-contained Pokemon TCG Kaggle Submission Agent
# Generated automatically by build_single_file.py

import json
import logging
import time
import sys
import csv
import datetime
from pathlib import Path
from typing import Any, Dict, List, Set, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# ==========================================
# CONSTANTS & EMBEDDED CONFIGURATIONS
# ==========================================

DELEGATION_MAP = {
  "turn_start": "hand_analyst",
  "after_hand_analysis": "turn_planner",
  "on_trigger": "strategy_agent",
  "on_opponent_play": "opponent_model",
  "before_turn_planner": "lethal_calculator",
  "always": "time_manager"
}

PRIORITY_RULES = {
  "_meta": {
    "version": "0.2.0",
    "description": "Ordered action-priority rules consumed by TurnPlanner. Rules are evaluated top-down; the first matching rule wins.",
    "fields": {
      "priority": "Evaluation order \u2014 lower number = higher priority",
      "action": "Canonical action label returned in the action list",
      "condition": "Human-readable trigger condition (evaluated by TurnPlanner logic)",
      "profile_tag": "Which priority_profile strings activate this rule ('*' = always active)",
      "rationale": "Why this action ranks here"
    }
  },
  "rules": [
    {
      "priority": 1,
      "action": "ATTACK_KO",
      "condition": "hand_score >= ko_threshold AND energy_sufficient",
      "profile_tag": "*",
      "rationale": "Taking a KO advances prize count \u2014 highest tempo play available."
    },
    {
      "priority": 2,
      "action": "EVOLVE",
      "condition": "evolution_card_in_hand AND base_on_bench",
      "profile_tag": "*",
      "rationale": "Evolving unlocks higher-damage attacks and abilities on the next turn."
    },
    {
      "priority": 3,
      "action": "ATTACH_ENERGY",
      "condition": "energy_card_in_hand AND active_or_bench_needs_energy",
      "profile_tag": "*",
      "rationale": "Energy attachment is once-per-turn; always use if available to build pressure."
    },
    {
      "priority": 4,
      "action": "PLAY_SUPPORTER",
      "condition": "supporter_card_in_hand AND no_supporter_played_this_turn",
      "profile_tag": "*",
      "rationale": "Supporters provide draw or search; one allowed per turn \u2014 play before trainers that may shuffle hand."
    },
    {
      "priority": 5,
      "action": "PLAY_TRAINER",
      "condition": "trainer_card_in_hand",
      "profile_tag": "*",
      "rationale": "Trainer cards provide draw, search, or disruption without spending the attack."
    },
    {
      "priority": 6,
      "action": "BENCH_POKEMON",
      "condition": "basic_pokemon_in_hand AND bench_not_full",
      "profile_tag": "*",
      "rationale": "Benching basics preserves future evolution lines and prevents auto-loss from empty bench."
    },
    {
      "priority": 7,
      "action": "PASS",
      "condition": "no_other_action_available",
      "profile_tag": "*",
      "rationale": "Fallback when no higher-priority action is legal this turn."
    }
  ],
  "profile_overrides": {
    "aggressive": {
      "description": "Maximise damage output; skip trainer plays that don't accelerate KO.",
      "boost": [
        "ATTACK_KO",
        "ATTACH_ENERGY"
      ],
      "suppress": []
    },
    "defensive": {
      "description": "Preserve resources; prioritise evolution and trainer cards.",
      "boost": [
        "EVOLVE",
        "PLAY_TRAINER",
        "PLAY_SUPPORTER"
      ],
      "suppress": []
    },
    "tempo": {
      "description": "Balance aggression and resource development.",
      "boost": [
        "BENCH_POKEMON",
        "EVOLVE"
      ],
      "suppress": []
    }
  }
}

STRATEGY_PROFILES = {
  "_meta": {
    "version": "0.1.0",
    "description": "Strategy profiles loaded by StrategyAgent. Each key maps to a posture, ordered actions, escalation action, and trigger description used for keyword matching."
  },
  "profiles": {
    "aggro": {
      "trigger": "prize race fast aggro attack pressure",
      "posture": "aggressive",
      "actions": [
        "ATTACK_KO",
        "ATTACH_ENERGY",
        "EVOLVE",
        "PLAY_TRAINER",
        "PASS"
      ],
      "escalation": "ATTACK_KO",
      "priority_profile": "aggressive"
    },
    "prize_race": {
      "trigger": "opponent prizes low close finish",
      "posture": "aggressive",
      "actions": [
        "ATTACK_KO",
        "PLAY_TRAINER",
        "ATTACH_ENERGY",
        "PASS"
      ],
      "escalation": "ATTACK_KO",
      "priority_profile": "aggressive"
    },
    "control": {
      "trigger": "disrupt stall discard trainer lock opponent",
      "posture": "defensive",
      "actions": [
        "PLAY_TRAINER",
        "ATTACH_ENERGY",
        "EVOLVE",
        "PASS"
      ],
      "escalation": "PLAY_TRAINER",
      "priority_profile": "defensive"
    },
    "setup": {
      "trigger": "bench early setup develop build",
      "posture": "tempo",
      "actions": [
        "EVOLVE",
        "ATTACH_ENERGY",
        "PLAY_TRAINER",
        "ATTACK_KO",
        "PASS"
      ],
      "escalation": "EVOLVE",
      "priority_profile": "tempo"
    },
    "endgame_close": {
      "trigger": "endgame own prizes two one close win",
      "posture": "aggressive",
      "actions": [
        "ATTACK_KO",
        "ATTACH_ENERGY",
        "PLAY_TRAINER",
        "PASS"
      ],
      "escalation": "ATTACK_KO",
      "priority_profile": "aggressive"
    },
    "bench_low": {
      "trigger": "bench count low single pokemon",
      "posture": "tempo",
      "actions": [
        "EVOLVE",
        "PLAY_TRAINER",
        "ATTACH_ENERGY",
        "PASS"
      ],
      "escalation": "PLAY_TRAINER",
      "priority_profile": "tempo"
    },
    "energy_stall": {
      "trigger": "energy stall attached zero no energy",
      "posture": "defensive",
      "actions": [
        "ATTACH_ENERGY",
        "PLAY_TRAINER",
        "PASS"
      ],
      "escalation": "ATTACH_ENERGY",
      "priority_profile": "defensive"
    },
    "hand_dead": {
      "trigger": "hand dead low score poor cards",
      "posture": "defensive",
      "actions": [
        "PLAY_TRAINER",
        "PASS"
      ],
      "escalation": "PASS",
      "priority_profile": "defensive"
    }
  }
}

DECK_ARCHETYPES = {
  "_meta": {
    "version": "0.2.0",
    "description": "Known deck archetypes used by opponent_model.py for Bayesian inference. signature_cards are card_ids that strongly indicate this archetype. typical_actions are ordered by likelihood per game phase."
  },
  "archetypes": {
    "aggro": {
      "signature_cards": [
        "chien-pao-ex-paf-061",
        "iron-hands-ex-par-070",
        "roaring-moon-ex-par-124",
        "koraidon-ex-sv1-125",
        "iron-valiant-ex-par-089"
      ],
      "card_pool": [
        "chien-pao-ex-paf-061",
        "baxcalibur-par-060",
        "frigibax-par-057",
        "arctibax-par-058",
        "iron-hands-ex-par-070",
        "roaring-moon-ex-par-124",
        "koraidon-ex-sv1-125",
        "irida-ast-186",
        "superior-energy-retrieval-paf-101",
        "nest-ball-sv1-255",
        "ultra-ball-sv1-196",
        "professor-s-research-sv1-190",
        "iono-pal-185",
        "iron-valiant-ex-par-089",
        "basic-water-energy",
        "basic-darkness-energy",
        "basic-fighting-energy"
      ],
      "typical_actions": {
        "early": [
          "attach_energy",
          "evolve",
          "attack"
        ],
        "mid": [
          "attack",
          "attach_energy",
          "play_supporter"
        ],
        "late": [
          "attack",
          "use_ability"
        ]
      },
      "avg_energy_per_attacker": 2,
      "prize_race_priority": 0.9,
      "bench_fill_rate": 0.6
    },
    "control": {
      "signature_cards": [
        "sableye-lof-070",
        "pecharunt-ex-pre-013",
        "comfey-lof-079",
        "path-to-the-peak-cre-148",
        "lost-vacuum-lof-096"
      ],
      "card_pool": [
        "sableye-lof-070",
        "comfey-lof-079",
        "pecharunt-ex-pre-013",
        "colress-experiment-lof-155",
        "mirage-gate-lof-163",
        "lost-vacuum-lof-096",
        "path-to-the-peak-cre-148",
        "iono-pal-185",
        "judge-fsf-108",
        "crushing-hammer-sv1-168",
        "hand-trimmer-sv6-161",
        "basic-psychic-energy",
        "basic-fire-energy"
      ],
      "typical_actions": {
        "early": [
          "play_trainer",
          "play_supporter",
          "attach_energy"
        ],
        "mid": [
          "play_trainer",
          "disrupt",
          "use_ability"
        ],
        "late": [
          "disrupt",
          "stall",
          "play_trainer"
        ]
      },
      "avg_energy_per_attacker": 1,
      "prize_race_priority": 0.3,
      "bench_fill_rate": 0.3
    },
    "combo": {
      "signature_cards": [
        "charizard-ex-obs-125",
        "pidgeot-ex-obs-164",
        "gardevoir-ex-sv1-086",
        "lugia-v-asr-138",
        "archeops-sit-147"
      ],
      "card_pool": [
        "charizard-ex-obs-125",
        "charmeleon-obs-007",
        "charmander-obs-023",
        "pidgeot-ex-obs-164",
        "pidgey-obs-162",
        "pidgeotto-obs-163",
        "gardevoir-ex-sv1-086",
        "kirlia-sv1-068",
        "ralts-sv1-067",
        "lugia-v-asr-138",
        "archeops-sit-147",
        "rare-candy-sv1-191",
        "arven-pal-186",
        "professor-s-research-sv1-190",
        "ultra-ball-sv1-196",
        "nest-ball-sv1-255",
        "basic-fire-energy",
        "basic-psychic-energy"
      ],
      "typical_actions": {
        "early": [
          "play_supporter",
          "play_trainer",
          "bench_pokemon"
        ],
        "mid": [
          "use_ability",
          "evolve",
          "attach_energy"
        ],
        "late": [
          "attack",
          "use_ability",
          "play_trainer"
        ]
      },
      "avg_energy_per_attacker": 3,
      "prize_race_priority": 0.6,
      "bench_fill_rate": 0.8
    },
    "utility": {
      "signature_cards": [
        "mew-ex-lof-151",
        "genesect-v-cel-185",
        "sylveon-ex-sv6-086",
        "eevee-sv1-120",
        "radiant-greninja-ast-046"
      ],
      "card_pool": [
        "mew-ex-lof-151",
        "genesect-v-cel-185",
        "mewtwo-v-pr-123",
        "sylveon-ex-sv6-086",
        "eevee-sv1-120",
        "radiant-greninja-ast-046",
        "power-tablet-fst-236",
        "elesa-s-sparkle-fst-233",
        "iono-pal-185",
        "ultra-ball-sv1-196",
        "nest-ball-sv1-255",
        "professor-s-research-sv1-190",
        "basic-psychic-energy",
        "double-turbo-energy-brg-151"
      ],
      "typical_actions": {
        "early": [
          "draw",
          "play_supporter",
          "bench_pokemon"
        ],
        "mid": [
          "play_trainer",
          "attach_energy",
          "evolve"
        ],
        "late": [
          "attack",
          "play_supporter",
          "use_ability"
        ]
      },
      "avg_energy_per_attacker": 2,
      "prize_race_priority": 0.5,
      "bench_fill_rate": 0.5
    }
  }
}

DECK_EV_SCORES = {
  "Ho-Oh": 0.2857,
  "Basic {F} Energy": 0.0,
  "Hop\u2019s Snorlax": 0.4,
  "Alolan Exeggutor ex": 0.4286,
  "Mega Clefable ex": 0.3429,
  "Koraidon": 0.3143,
  "Aurorus": 0.4286,
  "Ceruledge ex": 0.8,
  "Gholdengo": 0.2857,
  "Zacian ex": 0.6,
  "Crustle": 0.3429,
  "Jolteon ex": 0.8,
  "Yanmega ex": 0.6,
  "Basic {W} Energy": 0.0,
  "Tapu Koko": 0.3714,
  "Mega Starmie ex": 0.6,
  "Abomasnow": 0.3429,
  "Galarian Obstagoon": 0.4571,
  "Raichu": 0.4286,
  "Klinklang": 0.3429,
  "Rotom ex": 0.3714,
  "Eelektross": 0.2857,
  "Pinsir": 0.2857,
  "Team Rocket's Muk": 0.2857,
  "Sylveon": 0.2857,
  "Dragapult ex": 0.5714,
  "Mega Emboar ex": 0.9143,
  "Basic {P} Energy": 0.0,
  "Cornerstone Mask Ogerpon": 0.2857,
  "Dustox": 0.2857,
  "Blaziken ex": 0.5714,
  "Mega Kangaskhan ex": 0.5714,
  "Prism Energy": 0.2857,
  "Team Rocket's Moltres ex": 0.3143,
  "Duraludon": 0.3714,
  "Dusknoir": 0.4286,
  "Mega Eelektross ex": 0.5429,
  "Mega Abomasnow ex": 0.5714,
  "Krookodile": 0.4571,
  "Dhelmise": 0.3714,
  "Pikachu ex": 0.6286,
  "Serperior": 0.2857,
  "Stunfisk ex": 0.2857,
  "Salamence ex": 0.8571,
  "Excadrill": 0.5143,
  "Team Rocket's Nidoqueen": 0.3714,
  "Yveltal ex": 0.6,
  "Melmetal": 0.3429,
  "Bloodmoon Ursaluna ex": 0.6857
}

DEFAULT_DECK = [
    721, 721, 722, 722, 722, 722, 723, 723, 723, 723,
    1092, 1121, 1121, 1145, 1145, 1163, 1163, 1219,
    1219, 1219, 1219, 1227, 1227, 1227, 1227, 1262,
    1262, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3
]

# ==========================================
# BASE AGENT
# ==========================================
"""
agents/base_agent.py

Defines the BaseAgent class that all Player and Opponent modeling agents inherit from.
This ensures a unified interface structure across the entire codebase.
"""

from typing import Any

class BaseAgent:
    def __init__(self, perspective_flag: str):
        """
        Initializes the agent.
        
        Parameters
        ----------
        perspective_flag : str
            Either 'player' or 'opponent' to mark state ownership.
        """
        self.perspective_flag = perspective_flag

    def receive(self, packet: Any) -> Any:
        """
        Processes an incoming packet and returns a response.
        Must be implemented by child classes.
        """
        raise NotImplementedError("Subclasses must implement receive()")

# ==========================================
# ROUTER / BUS
# ==========================================
"""
router/bus.py

Enforces the strict information boundaries between agents in the PTCG Agent System.
Provides a central message bus that matches event types and ensures sub-agents
only receive their permitted scoped packets.
"""

import json
import logging
from typing import Dict, Any, Callable
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Scoped Packet Schemas
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class HandAnalystPacket:
    hand: list[str]
    deck_remaining: int

@dataclass(frozen=True)
class TurnPlannerPacket:
    hand_score: float
    priority_profile: dict[str, Any]
    top_play: str = ""
    game_state: dict[str, Any] = None
    turn: int = 1

@dataclass(frozen=True)
class StrategyPacket:
    trigger: str
    board_summary: dict[str, Any]

@dataclass(frozen=True)
class TimePacket:
    time_elapsed: float
    time_limit: float

@dataclass(frozen=True)
class OpponentModelPacket:
    turn: int
    newly_played_cards: list[str]
    revealed_active_pokemon: str
    revealed_bench_count: int
    revealed_hand_size: int
    revealed_prizes_remaining: int
    revealed_discard: list[str]
    game_phase: str

@dataclass(frozen=True)
class LethalPacket:
    my_active_damage: int
    opponent_active_hp: int
    legal_attacks: list[str]


class RouterBus:
    def __init__(self, delegation_map: Dict[str, str], log_dir: str = "logs"):
        self.delegation_map = delegation_map
        self.registry: Dict[str, Callable[[Any], Any]] = {}
        self.log_file = Path(log_dir) / "action_log.json"
        # Strict mapping of who is allowed to receive what packet class names
        self.allowed_packets: Dict[str, set] = {
            "opponent_model": {"OpponentModelPacket"},
            "hand_analyst": {"HandAnalystPacket"},
            "turn_planner": {"TurnPlannerPacket"},
            "strategy_agent": {"StrategyPacket"},
            "time_manager": {"TimePacket"},
            "lethal_calculator": {"LethalPacket"}
        }

    def register_agent(self, agent_name: str, callback: Callable[[Any], Any], perspective_flag: str = None):
        """
        Registers an agent's receive callback.
        Verifies that agents modeling the opponent are marked with perspective_flag='opponent'.
        """
        if agent_name == "opponent_model" and perspective_flag != "opponent":
            raise ValueError("opponent_model must have perspective_flag='opponent'")
        self.registry[agent_name] = callback

    def dispatch(self, event_name: str, packet: Any) -> Any:
        """
        Dispatches a packet to the agent registered for the given event name,
        validating packet access rules.
        """
        target_agent = self.delegation_map.get(event_name)
        if not target_agent:
            raise ValueError(f"No agent delegated for event: {event_name}")

        callback = self.registry.get(target_agent)
        if not callback:
            raise ValueError(f"No callback registered for agent: {target_agent}")

        # Enforce boundary: Check class name of the packet against target_agent allowances
        packet_class_name = type(packet).__name__
        allowed = self.allowed_packets.get(target_agent, set())
        
        # Safe guard: Ensure agents do not receive the raw orchestrator state itself
        if packet_class_name in ("GameState", "OrchestratorState"):
            raise PermissionError(f"Agent {target_agent} is blocked from receiving full game state!")

        if packet_class_name not in allowed:
            raise PermissionError(
                f"Boundary Violation: Agent '{target_agent}' is not allowed to receive packet of type '{packet_class_name}'"
            )

        logger.debug(f"Routing {packet_class_name} to {target_agent} for event {event_name}")
        
        # Call the delegate
        response = callback(packet)
        
        # Log delegation details to action_log.json
        self._log_delegation(event_name, target_agent, packet_class_name)
        
        return response

    def _log_delegation(self, event_name: str, agent_name: str, packet_type: str):
        """Appends a delegation log entry to action_log.json."""
        log_entry = {
            "event": event_name,
            "agent_called": agent_name,
            "packet_type": packet_type
        }
        
        try:
            logs = []
            if self.log_file.exists():
                content = self.log_file.read_text(encoding="utf-8").strip()
                if content:
                    try:
                        logs = json.loads(content)
                        if not isinstance(logs, list):
                            logs = [logs]
                    except json.JSONDecodeError:
                        logs = []
            
            logs.append(log_entry)
            self.log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to log delegation to {self.log_file}: {e}")


# ==========================================
# SUB-AGENTS
# ==========================================
"""
agents/lethal_calculator.py

Calculates if lethal damage is on the board.
If my_active_damage >= opponent_active_hp, it overrides the TurnPlanner
and forces the attack to guarantee the win or prize advantage.
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

class LethalCalculator(BaseAgent):
    def __init__(self, log_dir: str = "logs", perspective_flag: str = "player"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"

    def receive(self, packet: Any) -> Any:
        """
        Receives a LethalPacket. 
        Calculates if lethal is possible. Returns an action_override if true.
        """
        my_damage = getattr(packet, "my_active_damage", 0)
        opp_hp = getattr(packet, "opponent_active_hp", 100)
        legal_attacks = getattr(packet, "legal_attacks", [])

        # If we have an attack available and we can KO the opponent's active
        if legal_attacks and my_damage >= opp_hp and my_damage > 0:
            attack_name = legal_attacks[0]
            action = f"attack:{attack_name}"
            reasoning = f"LethalCalculator found lethal: my_damage {my_damage} >= opponent_hp {opp_hp}. Forcing attack."
            
            response = {
                "action_override": action,
                "reasoning_chain": reasoning
            }
            self._log_reasoning(response)
            return response
            
        return {
            "action_override": None,
            "reasoning_chain": "No lethal found."
        }

    def _log_reasoning(self, response: dict):
        log_entry = {
            "agent": "LethalCalculator",
            "action_override": response.get("action_override"),
            "reasoning_chain": response.get("reasoning_chain")
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

"""
agents/hand_analyst.py

Scores the player's opening or active hand composition, determines current strategy
profile priorities, selects the top card option, and logs reasoning.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

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

"""
agents/turn_planner.py

Evaluates the priority rules matching the active hand profile, filters legal actions
against game_state limits, sorts sequences, and outputs action_sequence layouts.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class TurnPlanner(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "player"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        # Load priority rules on init only
        self.rules = self._load_priority_rules()
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"

    def _load_priority_rules(self) -> dict:
        return PRIORITY_RULES

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
        sorted_actions = self._sort_actions(candidates, priority_profile)

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

    def _sort_actions(self, candidates: List[str], profile: str) -> List[str]:
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

        def get_priority_rank(action: str) -> int:
            for rank, prefix in enumerate(order):
                if action.startswith(prefix):
                    return rank
            return len(order)

        # Sort based on rank prefix match, preserve secondary ordering
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

"""
agents/strategy_agent.py

Evaluates macro game states on key trigger events, selects high-level strategy profiles,
and reports dynamic directive states.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

class StrategyAgent(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "player"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        self.profiles = self._load_strategy_profiles()
        self.active_strategy = "aggro_push"
        self.last_triggered_turn = -1
        self.last_priority_profile = None
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"

    def _load_strategy_profiles(self) -> dict:
        return STRATEGY_PROFILES

    def receive(self, packet: Any) -> dict:
        """
        Accepts and processes StrategyPacket. Evaluates macro priorities when triggered.
        """
        if not isinstance(packet, StrategyPacket):
            raise TypeError(
                f"StrategyAgent received an illegal packet type: {type(packet).__name__}."
            )

        trigger = packet.trigger
        board_summary = packet.board_summary or {}

        # Read board state values safely
        my_prizes = board_summary.get("my_prizes_remaining", 6)
        opponent_prizes = board_summary.get("opponent_prizes_remaining", 6)
        opponent_confidence = board_summary.get("opponent_archetype_confidence", 0.0)
        priority_profile = board_summary.get("priority_profile", "aggro_push")
        turn_number = board_summary.get("turn_number", 1)
        my_active_hp = board_summary.get("my_active_hp", 100)
        opponent_archetype = board_summary.get("opponent_archetype", "unknown")
        bench_has_attacker = board_summary.get("bench_has_attacker", False)

        # Trigger logic conditions
        is_prize_gap = (my_prizes - opponent_prizes) >= 2
        is_deck_identified = opponent_confidence > 0.75
        is_hand_shift = (self.last_priority_profile is not None) and (priority_profile != self.last_priority_profile)
        is_explicit = trigger == "force_evaluate"
        is_turn_milestone = turn_number in (3, 6, 9, 12, 15)
        my_bench_count = board_summary.get('my_bench_count', 0)
        is_bench_advantage = my_bench_count >= 3 and opponent_prizes > 3

        should_trigger = is_prize_gap or is_deck_identified or is_hand_shift or is_explicit or is_turn_milestone or is_bench_advantage

        # Cache last profile state
        self.last_priority_profile = priority_profile

        if not should_trigger:
            response = {
                "new_strategy": self.active_strategy,
                "reasoning": "No trigger condition met",
                "triggered": False,
                "turn_triggered": turn_number
            }
            self._log_reasoning(turn_number, trigger, self.active_strategy, self.active_strategy, False, "No trigger condition met")
            return response

        # Strategy selection logic (in priority order)
        prev_strategy = self.active_strategy
        
        if opponent_prizes <= 2:
            new_strategy = 'closing'
        elif my_prizes >= 5 and opponent_prizes <= 3:
            new_strategy = 'aggro_push'  # desperation: far behind, must attack
        elif opponent_archetype == 'aggro' and my_prizes < opponent_prizes:
            new_strategy = 'stall'  # only stall when ahead in prizes
        elif opponent_prizes <= 2 and my_prizes > opponent_prizes:
            new_strategy = "aggro_push"
        elif my_active_hp < 30 and bench_has_attacker:
            new_strategy = "setup"
        elif opponent_archetype == "control":
            new_strategy = "disruption"
        else:
            new_strategy = self.active_strategy  # no change

        # Update instance state parameters
        self.active_strategy = new_strategy
        self.last_triggered_turn = turn_number

        reasoning = f"Evaluated new strategy {new_strategy} via trigger context check."
        
        response = {
            "new_strategy": new_strategy,
            "reasoning": reasoning,
            "triggered": True,
            "turn_triggered": turn_number
        }

        self._log_reasoning(turn_number, trigger, prev_strategy, new_strategy, True, reasoning)
        return response

    def _log_reasoning(self, turn: int, trigger_reason: str, prev_strat: str, 
                      new_strat: str, triggered: bool, reasoning: str):
        log_entry = {
            "turn_triggered": turn,
            "trigger_reason": trigger_reason,
            "previous_strategy": prev_strat,
            "new_strategy": new_strat,
            "triggered": triggered,
            "reasoning": reasoning
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
            logger.error(f"Failed to log strategy choice: {e}")

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
        return DECK_ARCHETYPES.get("archetypes", {})

    def receive(self, packet: Any) -> dict:
        """
        Accepts and processes OpponentModelPacket.
        """
        if not isinstance(packet, OpponentModelPacket):
            raise TypeError(
                f"OpponentModel received an illegal packet type: {type(packet).__name__}."
            )

        revealed_cards = getattr(packet, "revealed_cards", None) or getattr(packet, "newly_played_cards", [])
        turn_number = getattr(packet, "turn_number", None) or getattr(packet, "turn", 1)
        active_pokemon = getattr(packet, "active_pokemon", None) or getattr(packet, "revealed_active_pokemon", None)
        prizes_remaining = getattr(packet, "prizes_remaining", None) or getattr(packet, "revealed_prizes_remaining", 6)
        discard_pile = getattr(packet, "discard_pile", None) or getattr(packet, "revealed_discard", [])

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

"""
agents/time_manager.py

Monitors elapsed game time and forces speed thresholds or pass actions
as limits are approached to prevent timeout forfeits.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

class TimeManager(BaseAgent):
    def __init__(self, log_dir: str = "logs", perspective_flag: str = "player"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.time_limit = 600.0
        self.warning_threshold = 540.0
        self.force_pass_threshold = 570.0
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"

    def receive(self, packet: Any) -> dict:
        """
        Accepts and processes TimePacket. Returns timeout overrides.
        """
        # Type check validation
        if not isinstance(packet, TimePacket):
            raise TypeError(
                f"TimeManager received an illegal packet type: {type(packet).__name__}."
            )

        time_elapsed = getattr(packet, "time_elapsed", 0.0)
        
        # Negative or missing check
        if time_elapsed is None or time_elapsed < 0.0:
            time_elapsed = 0.0
            self._log_warning("Negative or missing time_elapsed in TimePacket. Treated as 0.0.")

        # Hardcoded limit enforcement
        limit = self.time_limit
        time_remaining = max(0.0, limit - time_elapsed)

        # Timeout state logical checks
        if time_elapsed < 540.0:
            status = "normal"
            action_override = None
            urgent = False
        elif 540.0 <= time_elapsed < 570.0:
            status = "warning"
            action_override = "fastest_legal_move"
            urgent = True
        elif 570.0 <= time_elapsed < 600.0:
            status = "critical"
            action_override = "pass"
            urgent = True
        else: # >= 600
            status = "timeout"
            action_override = "forfeit"
            urgent = True

        return {
            "status": status,
            "action_override": action_override,
            "time_remaining": round(time_remaining, 2),
            "urgent": urgent
        }

    def _log_warning(self, msg: str):
        logger.warning(msg)
        log_entry = {
            "turn": "n/a",
            "hand_score": 0.0,
            "priority_profile": "n/a",
            "top_play": "n/a",
            "reasoning_chain": f"TIME MANAGER WARNING: {msg}"
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
            logger.error(f"Failed to log warning: {e}")

# ==========================================
# ORCHESTRATOR
# ==========================================
"""
agents/orchestrator.py

Orchestrates the entire Pokémon TCG match turn-by-turn.
Maintains the full game state, routes packets sequentially to sub-agents via RouterBus,
evaluates TimeManager overrides first, and extracts public state views.
"""

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

class Orchestrator(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "player"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        # Load delegation_map.json on init only
        self.delegation_map = self._load_delegation_map()
        
        # Initialize RouterBus
        self.bus = RouterBus(self.delegation_map, log_dir=str(self.log_dir))
        
        # Initialize and register sub-agents
        self.hand_analyst = HandAnalyst(log_dir=str(self.log_dir), skills_dir=str(self.skills_dir))
        self.turn_planner = TurnPlanner(log_dir=str(self.log_dir), skills_dir=str(self.skills_dir))
        self.strategy_agent = StrategyAgent(log_dir=str(self.log_dir), skills_dir=str(self.skills_dir))
        self.opponent_model = OpponentModel(log_dir=str(self.log_dir), skills_dir=str(self.skills_dir))
        self.time_manager = TimeManager(log_dir=str(self.log_dir))
        self.lethal_calculator = LethalCalculator(log_dir=str(self.log_dir))

        self.bus.register_agent("hand_analyst", self.hand_analyst.receive)
        self.bus.register_agent("turn_planner", self.turn_planner.receive)
        self.bus.register_agent("strategy_agent", self.strategy_agent.receive)
        self.bus.register_agent("opponent_model", self.opponent_model.receive, perspective_flag="opponent")
        self.bus.register_agent("time_manager", self.time_manager.receive)
        self.bus.register_agent("lethal_calculator", self.lethal_calculator.receive)
        
        # Game states
        self.game_state = {}
        self.current_turn = 0
        self.time_start = None

    def _load_delegation_map(self) -> dict:
        return DELEGATION_MAP

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError(
            "Orchestrator does not receive routed packets — it orchestrates matches directly"
        )

    def start_game(self):
        """Sets start time and resets turn counts."""
        self.time_start = time.time()
        self.current_turn = 0
        # Reset opponent model state for new game
        self.opponent_model.revealed_state = []
        self.opponent_model.inferred_state = {}
        self.opponent_model.archetype_confidence = 0.0
        self.opponent_model.identified_archetype = "unknown"

    def run_turn(self, game_state: dict) -> str:
        """
        Executes one full turn cycle, matching checks 1-7 in order.
        """
        if self.time_start is None:
            raise RuntimeError("start_game() must be called before first run_turn()")

        # STEP 1: Update full game state
        self.game_state = game_state
        self.current_turn += 1
        time_elapsed = time.time() - self.time_start

        # STEP 2: Always check TimeManager first
        time_packet = TimePacket(time_elapsed=time_elapsed, time_limit=600.0)
        time_result = self.bus.dispatch("always", time_packet)
        if time_result.get("action_override") is not None:
            return time_result["action_override"]

        # STEP 2.5: Lethal Calculator check
        lethal_packet = LethalPacket(
            my_active_damage=game_state.get("my_active_damage", 0),
            opponent_active_hp=game_state.get("opponent_active_hp", 100),
            legal_attacks=game_state.get("legal_attacks", [])
        )
        lethal_result = self.bus.dispatch("before_turn_planner", lethal_packet)
        if lethal_result.get("action_override") is not None:
            return lethal_result["action_override"]

        # STEP 3: Check StrategyAgent trigger
        board_summary = {
            "my_prizes_remaining": game_state.get("my_prizes", 6),
            "opponent_prizes_remaining": game_state.get("opponent_prizes", 6),
            "my_active_hp": game_state.get("my_active_hp", 100),
            "opponent_active_hp": game_state.get("opponent_active_hp", 100),
            "turn_number": self.current_turn,
            "opponent_archetype": self.opponent_model.identified_archetype,
            "opponent_archetype_confidence": self.opponent_model.archetype_confidence,
            "bench_has_attacker": game_state.get("bench_has_attacker", False)
        }
        
        strategy_packet = StrategyPacket(
            trigger=self._check_trigger(),
            board_summary=board_summary
        )
        strategy_result = self.bus.dispatch("on_trigger", strategy_packet)
        active_strategy = strategy_result["new_strategy"]

        # STEP 4: Run HandAnalyst
        hand_packet = HandAnalystPacket(
            hand=game_state.get("my_hand", []),
            deck_remaining=game_state.get("my_deck_count", 60)
        )
        hand_result = self.bus.dispatch("turn_start", hand_packet)

        # STEP 5: Run TurnPlanner
        turn_packet = TurnPlannerPacket(
            hand_score=hand_result["hand_score"],
            priority_profile=hand_result["priority_profile"],
            top_play=hand_result["top_play"],
            game_state=self._get_public_state(),
            turn=self.current_turn
        )
        plan_result = self.bus.dispatch("after_hand_analysis", turn_packet)

        # STEP 6: Update OpponentModel if opponent played
        if game_state.get("opponent_last_play") and game_state.get("opponent_revealed"):
            opp_packet = OpponentModelPacket(
                turn=self.current_turn,
                newly_played_cards=game_state["opponent_revealed"],
                revealed_active_pokemon=game_state.get("opponent_active"),
                revealed_bench_count=len(game_state.get("opponent_bench", [])),
                revealed_hand_size=game_state.get("opponent_hand_count", 5),
                revealed_prizes_remaining=game_state.get("opponent_prizes", 6),
                revealed_discard=game_state.get("opponent_discard", []),
                game_phase="early" if self.current_turn < 5 else "mid"
            )
            self.bus.dispatch("on_opponent_play", opp_packet)

        # STEP 7: Return primary action
        return plan_result["primary_action"]

    def _get_public_state(self) -> dict:
        """Returns only publicly visible game information."""
        return {
            "my_hand_count": len(self.game_state.get("my_hand", [])),
            "my_deck_count": self.game_state.get("my_deck_count", 60),
            "my_prizes": self.game_state.get("my_prizes", 6),
            "my_active_pokemon": self.game_state.get("my_active_pokemon"),
            "my_bench": self.game_state.get("my_bench", []),
            "opponent_active": self.game_state.get("opponent_active"),
            "opponent_bench_count": len(self.game_state.get("opponent_bench", [])),
            "opponent_prizes": self.game_state.get("opponent_prizes", 6),
            "opponent_discard": self.game_state.get("opponent_discard", []),
            "turn_number": self.current_turn,
            "legal_attacks": self.game_state.get("legal_attacks", []),
            "legal_attachments": self.game_state.get("legal_attachments", []),
            "legal_bench": self.game_state.get("legal_bench", []),
            "legal_evolutions": self.game_state.get("legal_evolutions", []),
            "legal_trainers": self.game_state.get("legal_trainers", [])
        }

    def _check_trigger(self) -> str:
        my_prizes = self.game_state.get("my_prizes", 6)
        opponent_prizes = self.game_state.get("opponent_prizes", 6)
        if (opponent_prizes - my_prizes) >= 2:
            return "prize_gap"
        return "none"

# ==========================================
# MAIN AGENT INTERFACE
# ==========================================
# GLOBAL SETUP (runs once on load)
try:
    orchestrator = Orchestrator()
    orchestrator.start_game()
except Exception as global_err:
    logger.error(f"Global orchestrator initialization failed: {global_err}")
    orchestrator = None

def get_val(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)



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


def agent(observation, configuration=None):
    """
    Main Actuation Agent loop parsed by Kaggle Match runtimes.
    """
    # Check if legacy mock unit test is running
    legal_actions = get_val(observation, "legal_actions")
    select = get_val(observation, "select")
    step = get_val(observation, "step", 0)
    
    if legal_actions and select is None:
        return legal_actions[0]

    # Step 0: The environment requires a 60-card deck submission.
    if select is None:
        return DEFAULT_DECK

    options = get_val(select, "option", [])
    max_count = get_val(select, "maxCount", 1)

    # Simple fallback: select first N options
    fallback_action = list(range(min(max_count, len(options))))

    if orchestrator is None:
        return fallback_action

    try:
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
        options = get_val(select, "option", [])
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
            action_label = orchestrator.run_turn(game_state)

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
        _log_action_exception(e)
        return fallback_action


