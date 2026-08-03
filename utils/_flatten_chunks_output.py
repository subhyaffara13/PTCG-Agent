from typing import Any

def _flatten_chunks_output(
    chunks_output_: list[Any],
) -> tuple[list[tuple[Any, ...]], TreeSpec]:
    # chunks_output is a list of chunked outputs
    # flatten chunked outputs:
    flat_chunks_output: list[list[Any]] = []
    arg_spec: TreeSpec | None = None
    for output in chunks_output_:
        flat_output, arg_specs = tree_flatten(output)
        flat_chunks_output.append(flat_output)
        if arg_spec is None:
            arg_spec = arg_specs

    # transpose chunk dim and flatten structure
    # flat_output_chunks is flat list of chunks
    flat_output_chunks = list(zip(*flat_chunks_output))
    if arg_spec is None:
        raise AssertionError("arg_spec must not be None")
    return flat_output_chunks, arg_spec

