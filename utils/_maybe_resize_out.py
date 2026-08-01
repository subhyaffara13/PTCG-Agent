
def _maybe_resize_out(
    out: TensorLikeType,
    shape: ShapeType,
    memory_format: torch.memory_format | None = None,
):
    if _resize_output_check(out, shape):
        return out.resize_(shape, memory_format=memory_format)
    else:
        return out

