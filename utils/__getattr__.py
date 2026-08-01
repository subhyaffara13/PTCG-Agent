import logging

def __getattr__(name: str):
    if name == "HeuristicValueNetwork":
        from cb_agents.heuristic_value import HeuristicValueNetwork
        return HeuristicValueNetwork
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
