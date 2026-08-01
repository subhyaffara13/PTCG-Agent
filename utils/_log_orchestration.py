
def _log_orchestration(gs: dict[str, Any], decision: Any) -> None:
    entry: dict[str, Any] = {
        "timestamp":  datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds") + "Z",
        "agent":      "Orchestrator",
        "input_keys": sorted(gs.keys()),
        "output":     asdict(decision),
    }
    _log_buffer.append(entry)


def _log_orchestration(gs: dict[str, Any], decision: Any) -> None:
    entry: dict[str, Any] = {
        "timestamp":  datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds") + "Z",
        "agent":      "Orchestrator",
        "input_keys": sorted(gs.keys()),
        "output":     asdict(decision),
    }
    _log_buffer.append(entry)


def _log_orchestration(gs: dict[str, Any], decision: Any) -> None:
    entry: dict[str, Any] = {
        "timestamp":  datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds") + "Z",
        "agent":      "Orchestrator",
        "input_keys": sorted(gs.keys()),
        "output":     asdict(decision),
    }
    _log_buffer.append(entry)

