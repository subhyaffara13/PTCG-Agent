from typing import Any

def _concat_chunked_outputs(
    out_dims: out_dims_t,
    arg_spec: TreeSpec,
    flat_output_chunks: list[tuple[Any, ...] | None],
) -> list[Tensor]:
    # concat chunks on out_dim
    flat_out_dims = _broadcast_to_and_flatten(out_dims, arg_spec)
    if flat_out_dims is None:
        raise AssertionError("flat_out_dims must not be None")
    if len(flat_out_dims) != len(flat_output_chunks):
        raise AssertionError(
            f"len(flat_out_dims)={len(flat_out_dims)} != len(flat_output_chunks)={len(flat_output_chunks)}"
        )
    flat_output: list[Tensor] = []
    for idx, out_dim in enumerate(flat_out_dims):
        chunk = flat_output_chunks[idx]
        if chunk is None:
            raise AssertionError(f"chunk at index {idx} must not be None")
        flat_output.append(torch.cat(chunk, dim=out_dim))
        # release tensors
        flat_output_chunks[idx] = None

    return flat_output

