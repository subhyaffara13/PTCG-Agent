# Content for router/bus.py

BUS = """\
\"\"\"
router/bus.py
-------------
Central message bus for the PTCG multi-agent system.

Design contract
---------------
- The Orchestrator is the ONLY agent that holds full game state.
- Every other agent receives a scoped input packet -- no more, no less.
- Attempting to request data outside an agent's declared scope raises
  ScopeViolationError loudly so the bug surfaces immediately.
- Every delegation call is appended to logs/action_log.json.
\"\"\"

from __future__ import annotations

import json
import pathlib
import datetime
from typing import Any

Card      = str
GameState = dict[str, Any]
Packet    = dict[str, Any]


class ScopeViolationError(RuntimeError):
    \"\"\"Raised when an agent receives a field outside its packet schema.\"\"\"


class UnknownAgentError(KeyError):
    \"\"\"Raised when the Router is asked to dispatch to an unregistered agent.\"\"\"


PACKET_SCHEMAS: dict[str, frozenset[str]] = {
    "HandAnalyst": frozenset({"hand", "deck_remaining"}),
    "TurnPlanner": frozenset({"hand_score", "priority_profile"}),
    "StrategyAgent": frozenset({"trigger", "board_summary"}),
    "OpponentModel": frozenset({"revealed_cards", "turn_number", "archetype_confidence"}),
    "TimeManager": frozenset({"time_elapsed", "time_limit"}),
}

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_LOG_PATH     = _PROJECT_ROOT / "logs" / "action_log.json"


class Router:
    \"\"\"Routes scoped packets from the Orchestrator to downstream agents.

    Usage
    -----
        router = Router()
        packet = router.dispatch("HandAnalyst", {
            "hand": ["Charizard ex", "Rare Candy"],
            "deck_remaining": 42,
        })
    \"\"\"

    def __init__(self) -> None:
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not _LOG_PATH.exists() or _LOG_PATH.stat().st_size == 0:
            _LOG_PATH.write_text("[]", encoding="utf-8")

    def dispatch(self, agent_name: str, data: dict[str, Any]) -> Packet:
        \"\"\"Validate scope and deliver a scoped packet to agent_name.
        Raises UnknownAgentError for unregistered agents.
        Raises ScopeViolationError for out-of-scope keys.
        \"\"\"
        schema = self._get_schema(agent_name)
        packet = self._enforce_scope(agent_name, schema, data)
        self._log(agent_name, packet, status="ok")
        return packet

    def _get_schema(self, agent_name: str) -> frozenset[str]:
        if agent_name not in PACKET_SCHEMAS:
            raise UnknownAgentError(
                f"No packet schema registered for agent '{agent_name}'. "
                f"Registered agents: {list(PACKET_SCHEMAS.keys())}"
            )
        return PACKET_SCHEMAS[agent_name]
"""
