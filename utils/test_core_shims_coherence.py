
def test_core_shims_coherence():
    """
    Check that all "semi-public" members of `numpy._core` are also accessible
    from `numpy.core` shims.
    """
    import numpy.core as core

    for member_name in dir(np._core):
        # Skip private and test members. Also if a module is aliased,
        # no need to add it to np.core
        if (
            member_name.startswith("_")
            or member_name in ["tests", "strings"]
            or f"numpy.{member_name}" in PUBLIC_ALIASED_MODULES
        ):
            continue

        member = getattr(np._core, member_name)

        # np.core is a shim and all submodules of np.core are shims
        # but we should be able to import everything in those shims
        # that are available in the "real" modules in np._core, with
        # the exception of the namespace packages (__spec__.origin is None),
        # like numpy._core.include, or numpy._core.lib.pkgconfig.
        if (
            inspect.ismodule(member)
            and member.__spec__ and member.__spec__.origin is not None
        ):
            submodule = member
            submodule_name = member_name
            for submodule_member_name in dir(submodule):
                # ignore dunder names
                if submodule_member_name.startswith("__"):
                    continue
                submodule_member = getattr(submodule, submodule_member_name)

                core_submodule = __import__(
                    f"numpy.core.{submodule_name}",
                    fromlist=[submodule_member_name]
                )

                assert submodule_member is getattr(
                    core_submodule, submodule_member_name
                )

        else:
            assert member is getattr(core, member_name)

