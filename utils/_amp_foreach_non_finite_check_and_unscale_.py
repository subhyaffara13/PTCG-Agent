
def _amp_foreach_non_finite_check_and_unscale_(self, found_inf, inv_scale):
    torch._check(
        found_inf.numel() == 1, lambda: "found_inf must be a 1-element tensor."
    )
    torch._check(
        inv_scale.numel() == 1, lambda: "inv_scale must be a 1-element tensor."
    )
    torch._check(
        found_inf.dtype.is_floating_point,
        lambda: "found_inf must be a float tensor.",
    )
    torch._check(
        inv_scale.dtype.is_floating_point,
        lambda: "inv_scale must be a float tensor.",
    )

