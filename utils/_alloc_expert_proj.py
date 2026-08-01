
def _alloc_expert_proj(
    num_experts: int,
    proj_out: int,
    proj_in: int,
    weight_dtype: torch.dtype,
    sf_dtype: torch.dtype,
    weight_k_div: int = 1,
    sf_gran_n: int | None = None,
    sf_gran_k: int | None = None,
    min_sf_out: int = 1,
) -> tuple[nn.Parameter, nn.Parameter]:
    """Allocate `(weight, weight_scale_inv)` parameters for one expert projection.

    `weight_k_div` halves the K dim for FP4-packed storage (2 e2m1 values per byte).
    `sf_gran_n` / `sf_gran_k` set per-block (None → per-row/per-tensor) SF granularity.
    `min_sf_out` floors the SF tensor's output dim — used by the fused gate_up
    projection to keep room for both halves (pass `2`) even when `proj_out < sf_gran_n`
    would otherwise collapse the SF dim to 1.
    """
    weight_t = torch.empty(num_experts, proj_out, proj_in // weight_k_div, dtype=weight_dtype)
    weight = nn.Parameter(weight_t, requires_grad=weight_t.is_floating_point())
    sf_out = max(_cdiv(proj_out, sf_gran_n) if sf_gran_n is not None else 1, min_sf_out)
    sf_in = _cdiv(proj_in, sf_gran_k) if sf_gran_k is not None else 1
    sf_t = torch.empty(num_experts, sf_out, sf_in, dtype=sf_dtype)
    sf = nn.Parameter(sf_t, requires_grad=sf_t.is_floating_point())
    return weight, sf

