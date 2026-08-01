
def _make_var_reduction_prim(name: str, impl_aten, doc):
    """Creates a reduction prim."""
    return _make_prim(
        schema=f"{name}(Tensor inp, int[]? dims, float? correction=1, *, ScalarType? output_dtype=None) -> Tensor",
        meta=_var_reduction_meta,
        impl_aten=impl_aten,
        return_type=RETURN_TYPE.NEW,
        doc=doc,
    )

