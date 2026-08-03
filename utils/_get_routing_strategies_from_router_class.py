from typing import List

def _get_routing_strategies_from_router_class() -> List[str]:
    """
    Dynamically extract routing strategies from the Router class __init__ method.
    """
    # Get the __init__ signature
    sig = inspect.signature(Router.__init__)

    # Get the routing_strategy parameter
    routing_strategy_param = sig.parameters.get("routing_strategy")

    if routing_strategy_param and routing_strategy_param.annotation:
        # Extract Literal values using get_args
        literal_values = get_args(routing_strategy_param.annotation)
        if literal_values:
            return list(literal_values)

    raise ValueError("Unable to extract routing strategies from Router class")

