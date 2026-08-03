from typing import Any

def _parse_kwargs(df: DataFrame, **kwargs: Any) -> dict[str, Any]:
    # Parse `kwargs`, evaluating any expressions we encounter.
    return {
        key: val._eval_expression(df) if isinstance(val, Expression) else val
        for key, val in kwargs.items()
    }

