
def _get_output_multiplier(request_body: dict) -> int:
    output_multiplier = 1
    for key in ("n", "best_of"):
        value = _to_int(request_body.get(key))
        if value is not None:
            output_multiplier = max(output_multiplier, value)
    return output_multiplier

