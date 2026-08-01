
def unsafe_generate_fake_kernels(op_profiles: dict[str, set[OpProfile]]) -> Generator:
    """
    Registers a fake kernel based on the given operator profiles. This fake
    kernel registration will override any existing fake kernel registrations.

    The input is a dictionary mapping operator names to a set of operator
    profiles, which we will use to generate fake kernels. The operator profiles
    are a record of the input and output tensor metadata. Based on this
    information we will match a given input to the recorded profile, and return
    an output with the same metadata as in the recorded profile. If a profile
    doesn't exist then an exception will be thrown.

    The fake kernel generation is considered unsafe because it relies on the
    rigid, pre-defined operator profiles that do not account for potential
    variations in output behavior. Specifically, the generated kernels assume a
    fixed relationship between input and output ranks. However, in reality, it's
    possible that data-dependent operations may produce outputs of different
    ranks even when given inputs of the same rank. The generated fake kernels
    are inflexible and unable to accommodate these nuances, making them
    potentially unsafe.

    Args:
        op_profiles (dict[str, set[OpProfile]]): A dictionary mapping operator
            name to a set of operator profiles from which we will generate fake
            kernels.

    Examples:

        >>> # Example: Registering an op-profile from draft-export
        >>> import torch
        >>> from torch.export._draft_export import draft_export
        >>>
        >>> @torch.library.custom_op("mylib::foo", mutates_args=())
        >>> def foo(x: Tensor, y: Tensor) -> Tensor:
        >>>     return x + y
        >>>
        >>> class M(torch.nn.Module):
        >>>     def forward(self, a, b):
        >>>         res = torch.ops.mylib.foo(a, b)  # no fake impl
        >>>         return res
        >>>
        >>> ep = draft_export(M(), (torch.ones(3, 4), torch.ones(3, 4))
        >>>
        >>> with torch._library.fake_profile.unsafe_generate_fake_kernels(ep._report.op_profiles):
        >>>     decomp = ep.run_decompositions()

    """

    libs: list[torch.library.Library] = []
    # Stores old fake impls from custom ops declared through @custom_op
    old_fake_impls: dict[str, Callable] = {}
    for op_name, profiles in op_profiles.items():
        log.warning(
            "Registering fake profile for %s. This will override any existing "
            "fake kernel registration.",
            op_name,
        )

        op_name_split = op_name.split(".")
        namespace, op_name_str = op_name_split[0], op_name_split[1]
        op_str = f"{namespace}::{op_name_str}"

        fake_kernel = _generate_fake_kernel(op_str, profiles)

        if opdef := _maybe_get_opdef(op_str):
            # If the op is a CustomOpDef, save the existing abstract_fn so that
            # we can restore it after this contextmanager
            if opdef._abstract_fn is not None:
                old_fake_impls[op_str] = opdef._abstract_fn
            opdef.register_fake(fake_kernel)

        else:
            # Create a new library so that we can register a new fake impl.
            # These libraries will then be destroyed after the contextmanager,
            # which will automatically restore the previously registered fake
            # impls.
            newlib = torch.library.Library(namespace, "FRAGMENT")  # noqa: TOR901
            torch.library.register_fake(
                op_str, fake_kernel, lib=newlib, allow_override=True
            )
            libs.append(newlib)

    try:
        yield libs
    finally:
        # Destroying the libraries will automatically restore the previously
        # registered fake impls
        for lib in libs:
            lib._destroy()

        # Restore abstract_fns for CustomOpDefs
        for op_str, old_fake in old_fake_impls.items():
            opdef = _maybe_get_opdef(op_str)
            if opdef is None:
                raise AssertionError(f"opdef for {op_str} must not be None")
            opdef.register_fake(old_fake)

