
def _get_data(x: ir.TensorBox) -> ir.IRNode:
    if isinstance(x.data, ir.BaseView):
        # TensorBox -> *View -> StorageBox -> IRNode
        node = x.data.unwrap_view()
        assert isinstance(node, (ir.BaseView, ir.MutableBox))
        return node.data
    elif isinstance(x.data, ir.StorageBox):
        # TensorBox -> StorageBox -> IRNode
        return x.data.data
    else:
        raise AssertionError(
            "Expect the data attr of a `TensorBox` to be either "
            f"an `ir.BaseView` or `ir.StorageBox` (got {x.data})."
        )


def _get_data(a):
    if is_masked_tensor(a):
        return a._masked_data
    return a

