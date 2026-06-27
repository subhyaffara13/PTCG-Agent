# Second part of agents/orchestrator.py content

ORCHESTRATOR_B = """\
    def _step_plan(self, hand_result):
        pkt = self._router.dispatch("TurnPlanner", {
            "hand_score":       hand_result["hand_score"],
            "priority_profile": hand_result["priority_profile"],
        })
        return self._planner.plan(pkt)

    def _step_strategy(self, gs):
        pkt = self._router.dispatch("StrategyAgent", {
            "trigger":       gs.get("trigger", ""),
            "board_summary": gs.get("board_summary", {}),
        })
        return self._strategy.evaluate(pkt)

    def _step_opponent(self, gs):
        opp_pkt = OpponentModelPacket(
            turn                      = int(gs.get("turn_number", 1)),
            newly_played_cards        = gs.get("revealed_cards", []),
            opponent_active_pokemon   = gs.get("opponent_active_pokemon"),
            opponent_bench_count      = int(gs.get("opponent_bench_count", 0)),
            opponent_hand_size        = int(gs.get("opponent_hand_size", 0)),
            opponent_prizes_remaining = int(gs.get("opponent_prizes_remaining", 6)),
            opponent_discard          = gs.get("opponent_discard", []),
            game_phase                = gs.get("game_phase", "mid"),
        )
        self._router.dispatch("OpponentModel", {
            "revealed_cards":       gs.get("revealed_cards", []),
            "turn_number":          int(gs.get("turn_number", 1)),
            "archetype_confidence": float(gs.get("archetype_confidence", 0.0)),
        })
        return self._opponent.receive(opp_pkt)

    def _merge(self, gs, time_result, hand_result, plan_result, strat_result, opp_result):
        if strat_result["confidence"] >= 0.75:
            final_actions = strat_result["actions"]
        else:
            final_actions = [s["action"] for s in plan_result if s.get("viable", False)]
        if time_result["directive"] == "FAST_MOVE":
            final_actions = final_actions[:1] if final_actions else ["PASS"]
        primary_action = final_actions[0] if final_actions else "PASS"
        return TurnDecision(
            timing_directive           = time_result["directive"],
            time_remaining             = time_result["time_remaining"],
            hand_score                 = hand_result["hand_score"],
            priority_profile           = hand_result["priority_profile"],
            top_play                   = hand_result["top_play"],
            strategy                   = strat_result["strategy"],
            posture                    = strat_result["posture"],
            strategy_confidence        = strat_result["confidence"],
            predicted_opponent_action  = opp_result["predicted_next_action"],
            opponent_archetype         = opp_result["inferred_deck_type"],
            opponent_confidence        = opp_result["archetype_confidence"],
            final_actions              = final_actions,
            primary_action             = primary_action,
        )

    def _emergency_pass(self, time_result):
        return TurnDecision(
            timing_directive           = "FORCE_PASS",
            time_remaining             = time_result["time_remaining"],
            hand_score                 = 0.0,
            priority_profile           = "defensive",
            top_play                   = "(time emergency)",
            strategy                   = "time_critical",
            posture                    = "defensive",
            strategy_confidence        = 1.0,
            predicted_opponent_action  = "unknown",
            opponent_archetype         = "unknown",
            opponent_confidence        = 0.0,
            final_actions              = ["PASS"],
            primary_action             = "PASS",
        )

    def _log(self, gs, decision):
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry: dict[str, Any] = {
            "timestamp":  datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent":      "Orchestrator",
            "input_keys": sorted(gs.keys()),
            "output":     asdict(decision),
        }
        try:
            log: list[Any] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            log = []
        log.append(entry)
        _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
"""
