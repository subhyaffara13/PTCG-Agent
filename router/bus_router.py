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
    "HandAnalyst": frozenset({"hand", "deck_remaining", "discard", "board", "has_searched_deck"}),
    "TurnPlanner": frozenset({"hand_score", "priority_profile", "top_play", "game_state", "turn", "time_remaining"}),
    "StrategyAgent": frozenset({"trigger", "board_summary"}),
    "OpponentModel": frozenset({"revealed_cards", "turn_number", "archetype_confidence", "turn", "newly_played_cards", "revealed_active_pokemon", "revealed_bench_count", "revealed_hand_size", "revealed_prizes_remaining", "revealed_discard", "game_phase"}),
    "TimeManager": frozenset({"time_elapsed", "time_limit", "legal_actions"}),
    "LethalCalculator": frozenset({"my_active_damage", "opponent_active_hp", "legal_attacks", "opponent_active_id", "my_active_hp"}),
}

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_LOG_PATH = _PROJECT_ROOT / "logs" / "action_log.json"


class Router:
    def __init__(self) -> None:
        self.handlers = {}
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not _LOG_PATH.exists() or _LOG_PATH.stat().st_size == 0:
            _LOG_PATH.write_text("[]", encoding="utf-8")

    def register_handler(self, agent_name: str, handler_function: Any) -> None:
        self.handlers[agent_name] = handler_function

    def dispatch(self, agent_name: str, data: dict[str, Any]) -> Any:
        schema = self._get_schema(agent_name)
        packet = self._enforce_scope(agent_name, schema, data)
        self._log(agent_name, packet, status="ok")
        if agent_name in self.handlers:
            return self.handlers[agent_name](packet)
        return packet

    def _get_schema(self, agent_name: str) -> frozenset[str]:
        if agent_name not in PACKET_SCHEMAS:
            raise UnknownAgentError(
                f"No packet schema registered for agent '{agent_name}'. "
                f"Registered agents: {list(PACKET_SCHEMAS.keys())}"
            )
        return PACKET_SCHEMAS[agent_name]

    def _enforce_scope(self, agent_name: str, schema: frozenset[str], data: dict[str, Any]) -> Packet:
        import dataclasses
        if dataclasses.is_dataclass(data):
            data = dataclasses.asdict(data)
        elif hasattr(data, "model_dump"):
            data = data.model_dump()
        elif hasattr(data, "_asdict"):
            data = data._asdict()
        elif hasattr(data, "__dict__"):
            data = data.__dict__
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
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds") + "Z",
            "agent": agent_name,
            "status": status,
            "packet_keys": sorted(payload.keys()),
        }
        if detail:
            entry["detail"] = detail
        try:
            try:
                log: list[dict[str, Any]] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, FileNotFoundError):
                log = []
            log.append(entry)
            _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
        except Exception:
            pass
