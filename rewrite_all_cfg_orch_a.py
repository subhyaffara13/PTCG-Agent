# First part of agents/orchestrator.py content

ORCHESTRATOR_A = """\
\"\"\"
agents/orchestrator.py
----------------------
The Orchestrator is the ONLY agent that holds full game state.

Architecture contract
---------------------
- Owns the canonical GameState dict.
- Communicates with every other agent EXCLUSIVELY through router/bus.py.
- Never passes raw GameState to any agent; the Router enforces scoping.
- Assembles the final action decision by composing each agent's output.
- All delegation calls logged by the Router in logs/action_log.json.
- Orchestrator logs its own final decisions to logs/reasoning_log.json.

Turn lifecycle
--------------
    orchestrate(game_state) -> TurnDecision

    Step 1 - TimeManager:   check time; abort early if critically low
    Step 2 - HandAnalyst:   score hand, derive priority_profile
    Step 3 - TurnPlanner:   produce ordered action plan
    Step 4 - StrategyAgent: select board posture from trigger + board_summary
    Step 5 - OpponentModel: update archetype inference from revealed cards
    Step 6 - Merge:         compose final TurnDecision from all outputs
\"\"\"

from __future__ import annotations
import json
import pathlib
import datetime
from dataclasses import dataclass, field, asdict
from typing import Any

from router.bus import Router
from agents.hand_analyst   import HandAnalyst
from agents.turn_planner   import TurnPlanner
from agents.time_manager   import TimeManager
from agents.strategy_agent import StrategyAgent
from agents.opponent_model import OpponentModel, OpponentModelPacket

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_LOG_PATH     = _PROJECT_ROOT / "logs" / "reasoning_log.json"


@dataclass
class TurnDecision:
    timing_directive:          str
    time_remaining:            float
    hand_score:                float
    priority_profile:          str
    top_play:                  str
    strategy:                  str
    posture:                   str
    strategy_confidence:       float
    predicted_opponent_action: str
    opponent_archetype:        str
    opponent_confidence:       float
    final_actions:             list[str] = field(default_factory=list)
    primary_action:            str       = "PASS"


class Orchestrator:
    \"\"\"Owns full game state; coordinates all agents through the Router.

    Usage
    -----
        orch     = Orchestrator()
        decision = orch.orchestrate(game_state)
        print(decision.primary_action)
    \"\"\"

    def __init__(self) -> None:
        self._router   = Router()
        self._analyst  = HandAnalyst()
        self._planner  = TurnPlanner()
        self._timer    = TimeManager()
        self._strategy = StrategyAgent()
        self._opponent = OpponentModel()

    def orchestrate(self, game_state: dict[str, Any]) -> TurnDecision:
        time_result  = self._step_time(game_state)
        if time_result["directive"] == "FORCE_PASS":
            return self._emergency_pass(time_result)
        hand_result  = self._step_hand(game_state)
        plan_result  = self._step_plan(hand_result)
        strat_result = self._step_strategy(game_state)
        opp_result   = self._step_opponent(game_state)
        decision     = self._merge(game_state, time_result, hand_result, plan_result, strat_result, opp_result)
        self._log(game_state, decision)
        return decision
"""
