
def register_inductor_prims() -> None:
    """Register DTensor sharding strategies for inductor prims ops.

    Called lazily because inductor prims are created via make_prim() in
    torch._inductor.inductor_prims, which is imported after this module.
    """
    # TODO: handle other inductor prims ops that may need DTensor sharding
    # strategies (e.g. mul_rn, div_rn). Those are more complicated and not
    # necessarily pointwise.
    _register_single_dim_pointwise(prims.fma.default)

