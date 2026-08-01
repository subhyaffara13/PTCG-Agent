
def _boxes_remaining(state: Mapping[str, Any]) -> int:
    boxes = state.get("boxes") or []
    return sum(1 for row in boxes for cell in row if not cell)

