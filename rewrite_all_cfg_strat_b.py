# Second part of agents/strategy_agent.py content

STRATEGY_AGENT_B = """\
    def _board_signal_match(self, board_summary):
        prizes     = board_summary.get("prizes")
        bench      = board_summary.get("bench_count")
        score      = board_summary.get("hand_score")
        energy     = board_summary.get("energy_attached")
        opp_prizes = board_summary.get("opponent_prizes")
        if prizes is not None and int(prizes) <= 2:
            return "endgame_close"
        if opp_prizes is not None and int(opp_prizes) <= 2:
            return "prize_race"
        if bench is not None and int(bench) <= 1:
            return "bench_low"
        if energy is not None and int(energy) == 0:
            return "energy_stall"
        if score is not None and float(score) < 2.0:
            return "hand_dead"
        return None

    def _keyword_scan(self, trigger_lower):
        best_key, best_score = None, 0.0
        for key, profile in self._profiles.items():
            trigger_desc = profile.get("trigger", "").lower()
            words = [w.strip("(),<>=") for w in trigger_desc.split() if len(w) > 3]
            if not words:
                continue
            matched = sum(1 for w in words if w in trigger_lower)
            score   = matched / len(words)
            if score > best_score:
                best_score, best_key = score, key
        return best_key, best_score

    def _log(self, packet, matched_key, match_reason, result):
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry: dict[str, Any] = {
            "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent":     "StrategyAgent",
            "input":     packet,
            "reasoning": {
                "profiles_available": list(self._profiles.keys()),
                "matched_profile":    matched_key,
                "match_reason":       match_reason,
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
