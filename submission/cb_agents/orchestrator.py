"""
agents/orchestrator.py
Orchestrates the Pokémon TCG match. Routes packets to sub-agents.
"""
import logging
import time
from pathlib import Path
from typing import Any
from cb_agents.base_agent import BaseAgent
from router.bus import RouterBus
from cb_agents.orchestrator_state import load_delegation_map, initialize_and_register_agents
from cb_agents.orchestrator_run import execute_orchestrator_turn

class Orchestrator(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "player"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        from cb_agents.context import SharedContext
        self.context = SharedContext()
        self.delegation_map = load_delegation_map(self.skills_dir)
        self.bus = RouterBus(self.delegation_map, log_dir=str(self.log_dir))
        initialize_and_register_agents(self)
        
        from cb_agents.belief_tracker import BeliefTracker
        from factory.game_runner import DEFAULT_DECK
        default_deck_dict = {cid: DEFAULT_DECK.count(cid) for cid in set(DEFAULT_DECK)}
        self.belief_tracker = BeliefTracker(initial_deck=default_deck_dict)
        self.turn_planner.mcts.belief_tracker = self.belief_tracker
        self.time_start = None

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError("Orchestrator does not receive routed packets")

    def start_game(self):
        self.time_start = time.time()
        self.current_turn = 0
        self.opponent_model.revealed_state = []
        self.opponent_model.inferred_state = {}
        self.opponent_model.archetype_confidence = 0.0
        self.opponent_model.identified_archetype = "unknown"

    def run_turn(self, game_state: dict) -> str:
        if self.time_start is None:
            raise RuntimeError("start_game() must be called before first run_turn()")
        return execute_orchestrator_turn(self, game_state)

    def flush_all_logs(self):
        for agent in [self.bus, self.hand_analyst, self.turn_planner, self.strategy_agent, 
                      self.opponent_model, self.lethal_calculator, self.time_manager]:
            agent.flush_logs()
