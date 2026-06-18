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
from cb_agents.base_agent import BaseAgent
from router.bus import RouterBus, HandAnalystPacket, TurnPlannerPacket, StrategyPacket, TimePacket, LethalPacket
from cb_agents.hand_analyst import HandAnalyst
from cb_agents.turn_planner import TurnPlanner
from cb_agents.strategy_agent import StrategyAgent
from cb_agents.opponent_model import OpponentModel, OpponentModelPacket
from cb_agents.time_manager import TimeManager
from cb_agents.lethal_calculator import LethalCalculator

logger = logging.getLogger(__name__)

class Orchestrator(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "player"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        from cb_agents.context import SharedContext
        self.context = SharedContext()
        
        # Load delegation_map.json on init only
        self.delegation_map = self._load_delegation_map()
        
        # Initialize RouterBus
        self.bus = RouterBus(self.delegation_map, log_dir=str(self.log_dir))
        
        # Initialize and register sub-agents
        self.hand_analyst = HandAnalyst(log_dir=str(self.log_dir), skills_dir=str(self.skills_dir), shared_context=self.context)
        self.turn_planner = TurnPlanner(log_dir=str(self.log_dir), skills_dir=str(self.skills_dir), shared_context=self.context)
        self.strategy_agent = StrategyAgent(log_dir=str(self.log_dir), skills_dir=str(self.skills_dir), shared_context=self.context)
        self.opponent_model = OpponentModel(log_dir=str(self.log_dir), skills_dir=str(self.skills_dir), shared_context=self.context)
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
        path = self.skills_dir / "delegation_map.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                return data.get("delegation", {})
            except Exception as e:
                logger.error(f"Failed to read delegation_map.json: {e}")
        # Default fallback map matching skills/delegation_map.json
        return {
            "turn_start": "hand_analyst",
            "after_hand_analysis": "turn_planner",
            "on_trigger": "strategy_agent",
            "on_opponent_play": "opponent_model",
            "before_turn_planner": "lethal_calculator",
            "always": "time_manager"
        }

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

        # STEP 3: Run HandAnalyst
        hand_packet = HandAnalystPacket(
            hand=game_state.get("my_hand", []),
            deck_remaining=game_state.get("my_deck_count", 60),
            discard=game_state.get("my_discard", []),
            board=game_state.get("my_board", [])
        )
        hand_result = self.bus.dispatch("turn_start", hand_packet)

        # STEP 4: Check StrategyAgent trigger
        board_summary = {
            "my_prizes_remaining": game_state.get("my_prizes", 6),
            "opponent_prizes_remaining": game_state.get("opponent_prizes", 6),
            "my_active_hp": game_state.get("my_active_hp", 100),
            "opponent_active_hp": game_state.get("opponent_active_hp", 100),
            "turn_number": self.current_turn,
            "opponent_archetype": self.opponent_model.identified_archetype,
            "opponent_archetype_confidence": self.opponent_model.archetype_confidence,
            "bench_has_attacker": game_state.get("bench_has_attacker", False),
            "my_bench_count": len(game_state.get("my_bench", [])),
            "prized_probabilities": hand_result.get("prized_probabilities", {})
        }
        
        strategy_packet = StrategyPacket(
            trigger=self._check_trigger(),
            board_summary=board_summary
        )
        strategy_result = self.bus.dispatch("on_trigger", strategy_packet)
        active_strategy = strategy_result["new_strategy"]

        # STEP 5: Run TurnPlanner
        turn_packet = TurnPlannerPacket(
            hand_score=hand_result["hand_score"],
            priority_profile=active_strategy,
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
