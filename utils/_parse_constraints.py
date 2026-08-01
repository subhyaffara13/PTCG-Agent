
def _parse_constraints(constraints: str) -> tuple[int, int]:
    parts = [p.strip() for p in constraints.split(",")]
    n_outputs = sum(1 for p in parts if p.startswith("="))
    n_inputs = len(parts) - n_outputs
    return n_outputs, n_inputs

