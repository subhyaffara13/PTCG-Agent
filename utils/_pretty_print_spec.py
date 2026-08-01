
def _pretty_print_spec(spec: object) -> str:
    if spec is None:
        return "None"
    elif isinstance(spec, DTensorSpec):
        return "".join([str(p) for p in spec.placements])
    elif isinstance(spec, Sequence):
        return "(" + ", ".join([_pretty_print_spec(s) for s in spec]) + ")"
    else:
        raise RuntimeError(f"Unknown spec type to print: spec={spec}")

