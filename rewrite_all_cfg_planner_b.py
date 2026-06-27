# Second part of agents/turn_planner.py content

TURN_PLANNER_B = """\
    def _log(self, packet, active_rules, plan):
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry: dict[str, Any] = {
            "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent":     "TurnPlanner",
            "input":     packet,
            "reasoning": {"active_rules": [r["action"] for r in active_rules]},
            "output":    plan,
        }
        try:
            log: list[Any] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            log = []
        log.append(entry)
        _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
"""
