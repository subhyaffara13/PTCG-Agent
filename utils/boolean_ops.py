
def boolean_ops() -> tuple[str, ...]:
    return (
        "isinf",
        "isnan",
        "logical_not",
        "logical_and",
        "signbit",
        "and_",
        "le",
        "lt",
        "ge",
        "gt",
        "eq",
        "ne",
        "or_",  # TODO should remove this op
        "xor",
    )

