
def upsample_compute_output_size(input_size, output_size, scale_factors):
    spatial_dimensions = len(input_size) - 2
    if output_size is not None:
        torch._check(
            scale_factors is None,
            lambda: "Must specify exactly one of output_size and scale_factors",
        )
        torch._check(len(output_size) == spatial_dimensions, lambda: "")
        return output_size
    if scale_factors is not None:
        # NB: this isn't necessary lol
        torch._check(
            output_size is None,
            lambda: "Must specify exactly one of output_size and scale_factors",
        )
        torch._check(len(scale_factors) == spatial_dimensions, lambda: "")
        output_size = []
        for i, s in enumerate(scale_factors):
            if int(s) == s:
                output_size.append(input_size[i + 2] * int(s))
            else:
                output_size.append(sym_int(input_size[i + 2] * s))
        return output_size
    torch._check(
        False, lambda: "Must specify exactly one of output_size and scale_factors"
    )

