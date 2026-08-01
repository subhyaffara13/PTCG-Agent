
def _create_fallback_choice(
    op_overload: torch._ops.OpOverload,
) -> ExternKernelChoice:
    """Create or reuse fallback choice that calls the op eagerly.

    Since kwargs are passed at bind time via maybe_append_choice rather than
    baked into the kernel, the same ExternKernelChoice is reused across
    compilations for the same op_overload.
    """
    fallback_name = (
        f"{op_overload.name().replace('::', '_').replace('.', '_')}_fallback"
    )

    existing = ExternKernelChoice.lookup(fallback_name)
    if existing is not None:
        return existing

    return ExternKernelChoice(
        kernel=op_overload,
        name=fallback_name,
        has_out_variant=False,
        op_overload=op_overload,
        use_fallback_kernel=True,
    )

