from typing import Any

def remap_to_exec_graph(torch_cuda_graph: torch.cuda.CUDAGraph) -> None:
    """Remap annotation keys from capture graph ID to exec graph ID.

    During capture, toolsId encodes the capture graph's ID in the upper
    32 bits. After instantiation, the profiler uses the exec graph's ID.
    This function rewrites the keys so annotations match the trace.

    Must be called after the ``torch.cuda.graph()`` context exits.
    """
    if not _kernel_annotations:
        return

    exec_handle = _cuda_runtime.cudaGraphExec_t(  # pyrefly: ignore[missing-attribute]
        init_value=torch_cuda_graph.raw_cuda_graph_exec()
    )
    exec_graph_id = _check_cuda_bindings(
        _cuda_runtime.cudaGraphExecGetId(  # pyrefly: ignore[missing-attribute]
            exec_handle
        )
    )

    # Only remap annotations from the most recent capture graph.
    # Previously remapped annotations (from earlier captures) keep their
    # correct exec graph IDs.
    capture_graph_id = _last_capture_graph_id
    remapped: dict[int, list[Any]] = {}
    for tools_id, ann_list in _kernel_annotations.items():
        graph_id = tools_id >> 32
        if capture_graph_id is not None and graph_id != capture_graph_id:
            # Belongs to a different graph — keep as-is.
            remapped[tools_id] = ann_list
            continue
        node_id = tools_id & 0xFFFFFFFF
        new_tools_id = (exec_graph_id << 32) | node_id
        if new_tools_id in remapped:
            remapped[new_tools_id].extend(ann_list)
        else:
            remapped[new_tools_id] = list(ann_list)

    _kernel_annotations.clear()
    _kernel_annotations.update(remapped)

