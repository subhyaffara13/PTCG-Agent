
def _has_aliased_buffers(buffers: Sequence[IRNode]) -> bool:
    buffers = [
        buffer.unwrap_view() if isinstance(buffer, ReinterpretView) else buffer
        for buffer in buffers
    ]
    # assuming the same buffer is represented by the same IRNode object
    return len(OrderedSet(id(buffer) for buffer in buffers)) < len(buffers)

