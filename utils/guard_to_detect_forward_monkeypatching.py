
def guard_to_detect_forward_monkeypatching(
    source: Source | None, mod: torch.nn.Module
) -> None:
    # Users sometimes patch the forward method of a nn module instance to
    # perform optimizations like quantization. Though this is not a good
    # software practice, but python allows this and Dynamo needs to detect
    # this patching.
    #
    # One way to do this is to add an ID_MATCH guard on every function
    # getting inlined (https://github.com/pytorch/pytorch/pull/124975). But
    # this increased guard overhead by around 20%.
    #
    # To keep the guard overhead down, we just guard on the `forward` being
    # not present in the mod __dict__. The common case of patching forward
    # method adds `forward` in the instance __dict__, whereas the unpatched
    # `forward` sits in the type(mod).__dict__
    if source:
        if "forward" in mod.__dict__ and callable(mod.__dict__["forward"]):
            # Monkeypatched forward method, add an ID_MATCH guard on forward function
            fwd = mod.__dict__["forward"]
            forward_source = AttrSource(source, "forward")
            if type(fwd) is types.MethodType:
                forward_source = AttrSource(forward_source, "__func__")
            install_guard(forward_source.make_guard(GuardBuilder.CLOSURE_MATCH))
        else:
            # Common case - check that the forward key is absent in mod __dict__
            install_guard(
                source.make_guard(
                    functools.partial(
                        GuardBuilder.NOT_PRESENT_IN_GENERIC_DICT, attr="forward"
                    )
                )
            )

