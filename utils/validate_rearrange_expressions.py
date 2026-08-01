
def validate_rearrange_expressions(
    left: ParsedExpression, right: ParsedExpression, axes_lengths: Mapping[str, int]
) -> None:
    """Perform expression validations that are specific to the `rearrange` operation.

    Args:
        left (ParsedExpression): left-hand side expression
        right (ParsedExpression): right-hand side expression
        axes_lengths (Mapping[str, int]): any additional length specifications for dimensions
    """
    for length in axes_lengths.values():
        if (length_type := type(length)) is not int:
            raise TypeError(
                f"rearrange axis lengths must be integers, got: {length_type}"
            )

    if left.has_non_unitary_anonymous_axes or right.has_non_unitary_anonymous_axes:
        raise ValueError("rearrange only supports unnamed axes of size 1")

    difference = set.symmetric_difference(left.identifiers, right.identifiers)
    if len(difference) > 0:
        raise ValueError(
            f"Identifiers only on one side of rearrange expression (should be on both): {difference}"
        )

    unmatched_axes = axes_lengths.keys() - left.identifiers
    if len(unmatched_axes) > 0:
        raise ValueError(
            f"Identifiers not found in rearrange expression: {unmatched_axes}"
        )

