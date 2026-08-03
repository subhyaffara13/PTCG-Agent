from typing import Any

def _lazy_import_cost_calculator(name: str) -> Any:
    """Handler for cost calculator functions (completion_cost, cost_per_token, etc.)"""
    return _generic_lazy_import(name, _COST_CALCULATOR_IMPORT_MAP, "Cost calculator")

