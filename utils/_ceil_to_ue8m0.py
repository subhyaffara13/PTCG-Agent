
def _ceil_to_ue8m0(sf: torch.Tensor) -> torch.Tensor:
    """Round each fp32 SF up to the nearest power of 2 (zero mantissa).

    Mirrors `deep_gemm.utils.math.ceil_to_ue8m0`. On SM100 the kernel's
    `pack_fp32_into_ue8m0` cleanly extracts the biased exponent only when the
    mantissa is already zero — its inner shifts (`>> 15`, `>> 7`, `<< 1`)
    otherwise leak mantissa bits into adjacent UE8M0 byte slots and silently
    corrupt the SF. SM90 consumes raw fp32 SFs without going through this path.
    """
    int_view = sf.view(torch.int32)
    return (int_view + ((1 << 23) - 1)).bitwise_and_(~((1 << 23) - 1)).view(torch.float)

