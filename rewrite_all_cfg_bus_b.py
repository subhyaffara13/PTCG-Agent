# Second part of router/bus.py content

BUS_B = """\
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
            "timestamp":   datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent":       agent_name,
            "status":      status,
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
"""
