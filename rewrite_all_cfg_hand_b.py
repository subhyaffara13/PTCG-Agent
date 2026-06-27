# Second part of agents/hand_analyst.py content

HAND_ANALYST_B = """\
    def _log(self, hand, deck_remaining, scored_cards, result):
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry: dict[str, Any] = {
            "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent":     "HandAnalyst",
            "input":     {"hand": hand, "deck_remaining": deck_remaining},
            "reasoning": {
                "card_scores":   [{"card": n, "ev_score": e} for n, e in scored_cards],
                "unknown_cards": [n for n, e in scored_cards if e == 0.0],
            },
            "output": result,
        }
        try:
            log: list[Any] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            log = []
        log.append(entry)
        _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
"""
