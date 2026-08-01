
def check_out_variant(
    functional_op: torch._ops.OpOverload, expected_out_op: torch._ops.OpOverload
) -> None:
    """
    Checks that to_out_variant returns the expected out variant for a functional op.
    Raises AssertionError if the out variant is not valid.
    """
    out_op = to_out_variant(functional_op)
    if out_op is None:
        tagged_info = _get_out_variants_info(functional_op)
        raise AssertionError(
            f"We did not find an out variant for {functional_op}. Some common mistakes include:\n"
            "  1. The out variant is missing the torch.Tag.out_variant tag.\n"
            "  2. The out variant is not an overload of the original op (e.g., 'op.out' or 'op.overload_out') \n"
            "  3. The out variant's input arguments does not match the functional op's signature (excluding the mutable args).\n"
            "  4. The original operator is not functional.\n"
            f"Overloads tagged with out_variant:\n"
            f"{tagged_info or '  (none)'}"
        )
    if out_op != expected_out_op:
        raise AssertionError(
            f"to_out_variant({functional_op}) returned {out_op}, "
            f"but expected {expected_out_op}. "
            f"The out variant name does not match the functional op."
        )

