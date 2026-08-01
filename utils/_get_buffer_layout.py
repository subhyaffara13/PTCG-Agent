
def _get_buffer_layout(buf_name: str) -> "torch._inductor.ir.Layout":
    """Get the layout for a buffer, handling both scheduler buffers and graph inputs."""
    if V.graph.scheduler:
        layout = V.graph.scheduler.get_buffer_layout(buf_name)
    else:
        buffer = V.graph.try_get_buffer(buf_name)
        # output arg
        if not buffer:
            assert buf_name == V.kernel.output_node.name
            layout = V.kernel.output_node.layout
        else:
            layout = buffer.get_layout()
    return layout

