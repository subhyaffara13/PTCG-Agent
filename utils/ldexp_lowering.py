
def ldexp_lowering(x: TensorBox, n: TensorBox):
    ldexp_fn = ops_wrapper("ldexp")

    x_dtype = x.get_dtype()
    n_dtype = n.get_dtype()

    x_is_float = x_dtype.is_floating_point
    n_is_int = not n_dtype.is_floating_point and n_dtype != torch.bool

    if x_is_float and n_is_int:
        # Use native ldexp
        def compute_ldexp(x, n):
            return ldexp_fn(x, n)

        return make_pointwise(compute_ldexp)(x, n)
    else:
        # Fall back to decomposition: x * pow(2, n)
        out_dtype = torch.float32 if is_integer_type(x) else x_dtype

        def compute_fallback(x, n):
            n_out_type = ops.to_dtype(n, out_dtype)
            two = ops.constant(2.0, out_dtype)
            pow_result = ops.pow(two, n_out_type)
            return ops.mul(x, pow_result)

        return make_pointwise(
            compute_fallback,
            override_return_dtype=out_dtype,
        )(x, n)

