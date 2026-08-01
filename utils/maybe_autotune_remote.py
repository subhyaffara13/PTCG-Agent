
def maybe_autotune_remote(
    name: str, choices: list[ChoiceCaller], inputs: list[Buffer], layout: Layout
) -> TensorBox | None:
    """
    Used by an op (like `mm`) to determine if the op should be autotuned
    locally (returns None) or remotely (returns a placeholder Buffer).
    """
    if not config.distributed_max_autotune_gemm:
        return None

    if not (autotune_pg := get_autotune_pg()):
        return None

    if len(choices) <= 1:
        return None

    state = V.distributed_autotune_state
    index = state.autotuned_index
    state.autotuned_index += 1
    local = index % autotune_pg.size() == autotune_pg.rank()

    V.current_node.meta[_DISTRIBUTED_AUTOTUNE_KEY] = _DistributedAutotuneInfo(
        index, local
    )
    if local:
        state.autotuned_local_count += 1
        return None

    return torch._inductor.ir.TensorBox.create(
        _DistributedAutotuneBuffer(name, inputs, layout)
    )

