
def gets_generated_view_copy(f: NativeFunction) -> bool:
    # Only aliasing (view) operators get a copy variant.
    if not f.is_view_op:
        return False
    # We don't need to bother generating copy variants for CompositeImplicitAutograd ops,
    # because we can let them decompose into base view ops.
    if f.has_composite_implicit_autograd_kernel:
        return False
    # We also don't need to generate copy variants for inplace views.
    if "inplace_view" in f.tags:
        return False
    # Assume ops ending in _inverse have manually-defined copy variants
    # (e.g. slice_inverse() has the copy variant slice_scatter()).
    # We -could- probably generate these as well, but the codegen will be
    # slightly different, and hand-writing these few kernels keeps codegen
    # complexity lower.
    if f.func.name.name.base.endswith("_inverse"):
        return False
    return True

