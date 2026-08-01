
def constant_boundary_condition(
    x, fill_value, padding=None, pad_fill_value=1.0, dim=None
):
    h = x.get_size()[-dim:]
    x_loader = x.make_loader()
    # pyrefly: ignore [unsupported-operation]
    padding_h = padding or [0] * dim

    def load(index):
        prefix = index[:-dim]
        ih = index[-dim:]

        mask = functools.reduce(
            ops.and_,
            # pyrefly: ignore [bad-argument-type, no-matching-overload]
            [range_mask(ih[i], h[i] + padding_h[i], -padding_h[i]) for i in range(dim)],
        )
        return (
            ops.masked(
                mask,
                lambda: constant_boundary_condition(x, pad_fill_value, dim=dim)(
                    [*prefix, *ih]
                ),
                fill_value,
            )
            if padding
            else ops.masked(mask, lambda: x_loader([*prefix, *ih]), fill_value)
        )

    return load

