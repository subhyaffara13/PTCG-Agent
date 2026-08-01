
def try_match_insignificant_strides(
    tensor: IRNode,
    strides: Sequence[int | torch.SymInt],
) -> IRNode:
    """
    Tries to match the strides of the tensor to those in the meta_strides. Strides of insignificant
    dimensions - size 0 or 1 - will be updated.

    If there are real stride differences (NHWC vs NCHW), or the tensor is not realized, then the input will be returned
    """
    if not is_storage_and_layout(tensor):
        return tensor

    if all(
        V.graph.sizevars.statically_known_equals(s1, s2)
        for s1, s2 in zip(strides, tensor.get_stride())
    ):
        return tensor

    if not significant_strides_equal(strides, tensor.get_stride(), tensor.get_size()):
        return tensor

    storage, old_layout = as_storage_and_layout(tensor)
    new_stride = [*old_layout.stride]
    for i, s in enumerate(tensor.get_size()):
        if V.graph.sizevars.statically_known_leq(s, 1):
            new_stride[i] = strides[i]

    new_layout = FixedLayout(
        old_layout.device,
        old_layout.dtype,
        old_layout.size,
        new_stride,
        old_layout.offset,
        old_layout.is_pinned,
    )
    return TensorBox(ReinterpretView(data=storage, layout=new_layout))

