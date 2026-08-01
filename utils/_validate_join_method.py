
def _validate_join_method(method: str) -> None:
    if method not in ["left", "right", "inner", "outer"]:
        raise ValueError(f"do not recognize join method {method}")

