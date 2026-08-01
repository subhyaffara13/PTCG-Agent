
def _assert_keys_normalized(
    keys: set[ComboKey],
    input_shapes: tuple[tuple[int, ...], ...],
    output_shapes: tuple[tuple[int, ...], ...],
) -> None:
    """Assert all combo keys have trivial shards already normalized to Replicate."""
    for key in keys:
        if key != normalize_combo_key(key, input_shapes, output_shapes):
            raise AssertionError(
                f"Key {key} contains un-normalized trivial shards; "
                f"call normalize_combo_key before _compare_rules"
            )

