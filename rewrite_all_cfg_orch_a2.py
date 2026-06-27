# Third part of agents/orchestrator.py content (continuation of ORCHESTRATOR_A)

ORCHESTRATOR_A2 = """\
    def _step_time(self, gs):
        pkt = self._router.dispatch("TimeManager", {
            "time_elapsed": gs.get("time_elapsed", 0.0),
            "time_limit":   gs.get("time_limit",   600.0),
        })
        return self._timer.tick(pkt)

    def _step_hand(self, gs):
        pkt = self._router.dispatch("HandAnalyst", {
            "hand":           gs.get("hand", []),
            "deck_remaining": gs.get("deck_remaining", 0),
        })
        return self._analyst.analyse(pkt)
"""
