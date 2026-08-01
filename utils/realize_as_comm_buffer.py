
def realize_as_comm_buffer(
    x: ir.TensorBox,
    comm_buffer_type: ir.CommBufferType,
    group_name: "torch.distributed.distributed_c10d.GroupName",
) -> None:
    """
    Realize an input as a comm buffer of the specified `comm_buffer_type`.

    Specifically, this realizes the underlying buffer if it's still unrealized
    and changes the layout of the buffer to `ir.CommBufferLayout`.
    """
    x.realize()
    buffer = _get_data(x)
    assert isinstance(buffer, ir.Buffer)

    layout = buffer.get_output_spec()
    if isinstance(layout, ir.CommBufferLayout):
        return

    # The buffer may have already been frozen to FixedLayout if it was used
    # by another operation before the comm operation.
    if not isinstance(layout, (ir.FlexibleLayout, ir.FixedLayout)):
        raise AssertionError(
            "A buffer can only be realized as a comm buffer if it "
            f"has `FlexibleLayout` or `FixedLayout` (got {layout})."
        )

    if is_symbolic(buffer.get_numel()):
        raise AssertionError(
            "A buffer with symbolic shape cannot be converted to "
            f"a comm buffer (got {layout})."
        )

    buffer.layout = ir.CommBufferLayout(
        layout=layout,
        comm_buffer_type=comm_buffer_type,
        group_name=group_name,
    )

