from typing import Any

def codegen_reinterpret_view_helper(data):
    """
    Collapse a chain of ReinterpretView <- StorageBox
    <- ReinterpretView <- StorageBox.... <- buffer wrappers if every layer
    has the same offset as the innermost (base) buffer.

    Returns:
        (size, stride, offset, dtype, collapsible: bool)
    """
    if isinstance(data, ir.Buffer):
        lay = data.get_layout()
        return lay.size, lay.stride, lay.offset, lay.dtype, True

    layouts: list[Any] = []
    cur = data
    while isinstance(cur, (ir.TensorBox, ir.StorageBox, ir.ReinterpretView)):
        lay = cur.get_layout()
        if lay is None:
            return None, None, None, None, False
        layouts.append(lay)
        cur = cur.data  # unwrap

    if not isinstance(cur, ir.Buffer):
        return None, None, None, None, False

    # All wrapper offsets must match base offset to be collapsible
    for lay in layouts:
        if lay.offset != cur.get_layout().offset:
            return None, None, None, None, False

    base_lay = cur.get_layout()
    return base_lay.size, base_lay.stride, base_lay.offset, base_lay.dtype, True

