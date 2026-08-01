
def setup_megamoe_weights(module: torch.nn.Module) -> None:
    """One-shot pack + permute of an FP8Experts module's L1/L2 weights into the
    Mega MoE UTCCP layout. Called lazily on the first megamoe forward; idempotent
    via the caller's ``_megamoe_transformed`` flag.

    Steps:
      1. Cast UE8M0 SF → FP32 and call ``transform_sf_into_required_layout`` →
         packed int32 in MN-major TMA-aligned layout.
      2. Run ``transform_weights_for_mega_moe``: interleaves gate/up on L1 and
         transposes both SFs for UTCCP.
      3. Overwrite the loader-side parameters in place; the interleave preserves
         the ``[E_local, 2*I, *]`` leading dims so downstream ``.size(...)`` reads
         stay valid.

    Unwraps any ``DTensor`` wrappers FSDP2/EP may have placed around the loader-
    side Parameters — the kernel takes raw pointers.
    """
    deepgemm = load_deepgemm_kernel(requires_sm100=True)
    gate_up_sf_raw = to_local(module.gate_up_proj_scale_inv.data)
    down_sf_raw = to_local(module.down_proj_scale_inv.data)
    # Force int8 view: the kernel's interleave reshape/empty_like/copy_ is bit-level.
    gate_up_w = to_local(module.gate_up_proj.data).view(torch.int8).contiguous()
    down_w = to_local(module.down_proj.data).view(torch.int8).contiguous()

    intermediate_hidden = module.intermediate_dim
    num_local_experts = module.num_experts
    hidden_dim = module.hidden_dim

    if hidden_dim % 32 != 0 or intermediate_hidden % 32 != 0:
        raise ValueError(
            f"DeepGEMM Mega MoE requires `hidden_dim` and `intermediate_hidden` divisible by 32 "
            f"(FP8 SF granularity); got hidden_dim={hidden_dim}, intermediate_hidden={intermediate_hidden}."
        )

    gate_up_sf = deepgemm.transform_sf_into_required_layout(
        gate_up_sf_raw.float(),
        2 * intermediate_hidden,
        hidden_dim,
        recipe=(1, 32),
        num_groups=num_local_experts,
    )
    down_sf = deepgemm.transform_sf_into_required_layout(
        down_sf_raw.float(),
        hidden_dim,
        intermediate_hidden,
        recipe=(1, 32),
        num_groups=num_local_experts,
    )
    (gate_up, gate_up_sf), (down, down_sf) = deepgemm.transform_weights_for_mega_moe(
        (gate_up_w, gate_up_sf),
        (down_w, down_sf),
    )
    module.gate_up_proj = torch.nn.Parameter(gate_up, requires_grad=False)
    module.gate_up_proj_scale_inv = torch.nn.Parameter(gate_up_sf, requires_grad=False)
    module.down_proj = torch.nn.Parameter(down, requires_grad=False)
    module.down_proj_scale_inv = torch.nn.Parameter(down_sf, requires_grad=False)

