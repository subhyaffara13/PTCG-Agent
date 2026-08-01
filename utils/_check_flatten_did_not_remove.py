
def _check_flatten_did_not_remove(original, jit_flattened) -> None:
    """torch.jit._flatten removes None. Check if it did so in this case."""

    def flatten(x):
        if isinstance(x, (list, tuple)):
            for inner in x:
                yield from flatten(inner)
        elif isinstance(x, dict):
            for inner in x.values():
                yield from flatten(inner)
        else:
            yield x

    flattened_with_none = list(flatten(original))
    num_none = len(flattened_with_none) - len(jit_flattened)
    if num_none < 0:
        raise AssertionError(f"num_none must be >= 0, got {num_none}")
    if num_none:
        raise ValueError(
            f"args contained {num_none} None's after flattening. "
            "When exporting a ScriptModule or ScriptFunction, no args may "
            "be None because that breaks type propagation."
        )

