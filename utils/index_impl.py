
def index_impl(x, indices, check):
    output_size, inner_fn, _ = index_impl_helper(x, indices, check)

    return Pointwise.create(
        device=x.get_device(),
        dtype=x.get_dtype(),
        inner_fn=inner_fn,
        ranges=output_size,
    )

