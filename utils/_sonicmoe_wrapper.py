
def _sonicmoe_wrapper(
    hidden_states: torch.Tensor,
    router_scores: torch.Tensor,
    expert_ids: torch.Tensor,
    token_idx: torch.Tensor,
    w1: torch.Tensor,
    b1: torch.Tensor | None,
    w2: torch.Tensor,
    b2: torch.Tensor | None,
    act_name: str,
    num_experts: int,
    concat_layout: bool,
    is_inference_mode_enabled: bool,
) -> torch.Tensor:
    """Module-level shim around `moe_general_routing_inputs` so `allow_in_graph` can wrap it.

    sonicmoe asserts `not torch.compiler.is_compiling()` internally because it dispatches
    CuteDSL kernels, which Dynamo can't trace. `allow_in_graph` keeps the call in the FX
    graph as a single opaque node (no tracing into the body, no graph break) while still
    running the real Python at runtime — autograd through `_UpProjection` / `_DownProjection`
    flows normally. The decorator must be applied at module load time, not inside the compiled
    function — hence this shim plus the `allow_in_graph` decorator above.
    """
    sonicmoe = _load_sonicmoe_kernel()
    activation_type_enum = sonicmoe.activation_type_enum
    activation_type = getattr(
        activation_type_enum, ACT_MAP.get(act_name, "swiglu").upper(), activation_type_enum.SWIGLU
    )
    output, _ = sonicmoe.moe_general_routing_inputs(
        hidden_states,
        router_scores,
        token_idx,
        expert_ids,
        w1,
        b1,
        w2,
        b2,
        E=num_experts,
        activation_type=activation_type,
        is_inference_mode_enabled=is_inference_mode_enabled,
        concat_layout=concat_layout,
        stream_id=None,
    )
    return output

