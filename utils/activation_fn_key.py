
def activation_fn_key(value: str):
    """Ensures that `value` is a string corresponding to an activation function."""
    # TODO (joao): in python 3.11+, we can build a Literal type from the keys of ACT2FN
    if len(ACT2FN) > 0:  # don't validate if we can't import ACT2FN
        if value not in ACT2FN:
            raise ValueError(
                f"Value must be one of {list(ACT2FN.keys())}, got {value}. "
                "Make sure to use a string that corresponds to an activation function."
            )

