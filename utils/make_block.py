
def make_block(
    values, placement, klass=None, ndim=None, dtype: Dtype | None = None
) -> Block:
    """
    This is a pseudo-public analogue to blocks.new_block.

    We ask that downstream libraries use this rather than any fully-internal
    APIs, including but not limited to:

    - core.internals.blocks.make_block
    - Block.make_block
    - Block.make_block_same_class
    - Block.__init__
    """
    warnings.warn(
        # GH#56815
        "make_block is deprecated and will be removed in a future version. "
        "Use pd.api.internals.create_dataframe_from_blocks or "
        "(recommended) higher-level public APIs instead.",
        Pandas4Warning,
        stacklevel=2,
    )

    if dtype is not None:
        dtype = pandas_dtype(dtype)

    values, dtype = extract_pandas_array(values, dtype, ndim)

    from pandas.core.internals.blocks import ExtensionBlock

    if klass is ExtensionBlock and isinstance(values.dtype, PeriodDtype):
        # GH-44681 changed PeriodArray to be stored in the 2D
        # NDArrayBackedExtensionBlock instead of ExtensionBlock
        # -> still allow ExtensionBlock to be passed in this case for back compat
        klass = None

    if klass is None:
        dtype = dtype or values.dtype
        klass = get_block_type(dtype)

    elif klass is _DatetimeTZBlock and not isinstance(values.dtype, DatetimeTZDtype):
        # pyarrow calls get here (pyarrow<15)
        values = DatetimeArray._simple_new(
            # error: Argument "dtype" to "_simple_new" of "DatetimeArray" has
            # incompatible type "Union[ExtensionDtype, dtype[Any], None]";
            # expected "Union[dtype[datetime64], DatetimeTZDtype]"
            values,
            dtype=dtype,  # type: ignore[arg-type]
        )

    if not isinstance(placement, BlockPlacement):
        placement = BlockPlacement(placement)

    ndim = _maybe_infer_ndim(values, placement, ndim)
    if isinstance(values.dtype, (PeriodDtype, DatetimeTZDtype)):
        # GH#41168 ensure we can pass 1D dt64tz values
        # More generally, any EA dtype that isn't is_1d_only_ea_dtype
        values = extract_array(values, extract_numpy=True)
        values = ensure_block_shape(values, ndim)

    check_ndim(values, placement, ndim)
    values = maybe_coerce_values(values)
    return klass(values, ndim=ndim, placement=placement)


def make_block(ops: list[Op]) -> BasicBlock:
    block = BasicBlock()
    block.ops.extend(ops)
    return block

