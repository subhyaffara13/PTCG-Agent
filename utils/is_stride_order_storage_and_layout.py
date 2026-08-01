
def is_stride_order_storage_and_layout(
    x: IRNode, stride_order: Sequence[int | Integer]
) -> bool:
    try:
        _buffer, layout = as_storage_and_layout(x, freeze=False)
        return layout.is_stride_ordered(stride_order)
    except NotImplementedError:
        return False

