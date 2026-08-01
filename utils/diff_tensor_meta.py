
def diff_tensor_meta(
    meta1: TensorMetadata, meta2: TensorMetadata, check_grad=True
) -> list[str]:
    from torch.fx.experimental.symbolic_shapes import GuardOnDataDependentSymNode

    pair_diffs = []
    for meta_name in TensorMetadata._fields:
        if not check_grad and meta_name == "requires_grad":
            continue
        val1 = getattr(meta1, meta_name)
        val2 = getattr(meta2, meta_name)
        try:
            if val1 != val2:
                pair_diffs.append(f"'{meta_name}: {val1} vs {val2}'")
        except GuardOnDataDependentSymNode:
            pair_diffs.append(f"'{meta_name}: {val1} vs {val2}'")
            continue
    return pair_diffs

