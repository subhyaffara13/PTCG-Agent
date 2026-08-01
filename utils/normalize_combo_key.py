
def normalize_combo_key(
    combo_key: ComboKey,
    input_shapes: tuple[tuple[int, ...], ...],
    output_shapes: tuple[tuple[int, ...], ...],
) -> ComboKey:
    """
    Normalize a combo_key by converting trivial shards to Replicate.

    This deduplicates equivalent placement combinations, e.g.:
    - P(max) -> S(0) on output [1,1,1] becomes P(max) -> R
    - S(0), R -> R on input [1,4] becomes R, R -> R

    Args:
        combo_key: (input_placement_strs, output_placement_strs) tuple
        input_shapes: Shapes of input tensors
        output_shapes: Shapes of output tensors

    Returns:
        Normalized combo_key with trivial shards converted to Replicate
    """
    input_placement_strs, output_placement_strs = combo_key

    normalized_inputs = tuple(
        normalize_placement_str(p_str, shape)
        for p_str, shape in zip(input_placement_strs, input_shapes)
    )

    normalized_outputs = tuple(
        normalize_placement_str(p_str, shape)
        for p_str, shape in zip(output_placement_strs, output_shapes)
    )

    return (normalized_inputs, normalized_outputs)

