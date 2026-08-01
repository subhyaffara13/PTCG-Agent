
def view_as_complex_single_dim_strategy(op, args_schema, kwargs_schema):
    # view_as_complex: float [..., 2] -> complex [...]
    # Dims 0..ndim-2 map 1:1; last dim (real/imag pair) is consumed.
    # P(max)/P(min) invalid: complex numbers have no total ordering.
    input_meta = args_schema[0]
    if not isinstance(input_meta, TensorMeta):
        raise AssertionError(f"Expected TensorMeta, got {type(input_meta)}")
    ndim = len(input_meta.shape)
    strategies: list[list[Placement | _ShardingPlaceholder]] = []
    for d in range(ndim - 1):
        strategies.append([_ShardingPlaceholder(d), _ShardingPlaceholder(d)])
    strategies.append([Partial("sum"), Partial("sum")])
    strategies.append([Partial("avg"), Partial("avg")])
    return strategies

