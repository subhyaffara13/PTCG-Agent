
def autograd_would_have_decomposed(
    func: torch._ops.OpOverload, flat_args: Sequence[torch.Tensor | object]
) -> bool:
    """
    Suppose that an operator has CompositeImplicitAutograd decomp registered.
    Would autograd have used this decomposition?  It will only use it if there
    isn't an explicit backend registration for the device as well.  This function
    will tell if this would have occurred.

    Why do we need to apply these decompositions later?  When inference mode is
    on, the autograd key is bypassed entirely, so a lower level mode cannot rely
    on the decomposition have been applied.  It's easy to accidentally never apply
    the decomposition, resulting in an operator showing up in a graph that
    is unexpected.

    Why do we need to AVOID applying the decomposition when autograd wouldn't
    have decomposed?  If autograd doesn't decompose, this means in eager mode
    we would have run the fused kernel.  It must be possible to trace this
    fused kernel directly into the graph for fidelity with eager (NB: a user
    has the option of then further decomposing at proxy tensor mode via
    decomposition table, but we must preserve it to proxy mode to have the
    choice.)

    Why does functionalization need to also perform the test here?  This is
    because some CompositeImplicitAutograd decompositions are not functional.
    If we are eventually going to decompose, we need to do this while we can
    still turn functionalization back on, so those decompositions get functionalized.
    So an early decomposition in functionalization may still be necessary.  Note that
    if proxy tensor decomposition process could turn functionalization back on, this
    wouldn't be necessary, and maybe that is a useful thing to do anyway because
    the decomposition table is user specified and a user could violate the functional
    decomp requirement with a bad decomp.  If this happened, then you could always
    pass through functionalization.
    """
    has_backend_registration = False
    for a in flat_args:
        if isinstance(a, torch.Tensor):
            backend_key = torch._C._parse_dispatch_key(
                torch._C._dispatch_key_for_device(a.device.type)
            )
            if backend_key is None:
                raise AssertionError(
                    f"failed to parse dispatch key for device {a.device.type}"
                )
            # TODO: use func.has_kernel_for_dispatch_key(backend_key)
            # but this one checks py_impl and CompositeImplicitAutograd
            # incorrectly shows up as has backend reg here
            has_backend_registration = torch._C._dispatch_has_kernel_for_dispatch_key(
                func.name(), backend_key
            )

            # in theory we should take all backend keys and take the highest priority one
            # to properly mimic the dispatcher,
            # this just grabs the first tensor and takes its device key
            break
    return not has_backend_registration

