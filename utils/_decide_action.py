
def _decide_action(reasons):
    joined = "".join(reasons).lower()
    return "trigger_deck_optimizer" if "win rate" in joined else "trigger_strategy_optimizer"

