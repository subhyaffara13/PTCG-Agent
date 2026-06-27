from __future__ import annotations
import json
import pathlib
import datetime
from typing import Any

Card = str
GameState = dict[str, Any]
Packet = dict[str, Any]


class ScopeViolationError(RuntimeError):
    pass


class UnknownAgentError(KeyError):
    pass


PACKET_SCHEMAS: dict[str, frozenset[str]] = {
    "HandAnalyst": frozenset({"hand", "deck_remaining"}),
    "TurnPlanner": frozenset({"hand_score", "priority_profile"}),
    "StrategyAgent": frozenset({"trigger", "board_summary"}),
    "OpponentModel": frozenset({"revealed_cards", "turn_number", "archetype_confidence"}),
    "TimeManager": frozenset({"time_elapsed", "time_limit"}),
}

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_LOG_PATH = _PROJECT_ROOT / "logs" / "action_log.json"


class Router:
    def __init__(self) -> None:
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not _LOG_PATH.exists() or _LOG_PATH.stat().st_size == 0:
            _LOG_PATH.write_text("[]", encoding="utf-8")

    def dispatch(self, agent_name: str, data: dict[str, Any]) -> Packet:
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

    def _enforce_scope(self, agent_name: str, schema: frozenset[str], data: dict[str, Any]) -> Packet:
        incoming_keys = frozenset(data.keys())
        forbidden = incoming_keys - schema
        if forbidden:
            self._log(agent_name, data, status="scope_violation",
                      detail=f"Forbidden keys: {sorted(forbidden)}")
            raise ScopeViolationError(
                f"Agent '{agent_name}' was sent field(s) outside its packet schema: "
                f"{sorted(forbidden)}. Allowed keys: {sorted(schema)}"
            )
        return {k: data[k] for k in schema if k in data}

    def _log(self, agent_name: str, payload: dict[str, Any], *, status: str, detail: str | None = None) -> None:
        entry: dict[str, Any] = {
            "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent": agent_name,
            "status": status,
            "packet_keys": sorted(payload.keys()),
        }
        if detail:
            entry["detail"] = detail
        try:
            log: list[dict[str, Any]] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            log = []
        log.append(entry)
        _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
