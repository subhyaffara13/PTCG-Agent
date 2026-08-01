
def _advise_is_size(a: SymInt) -> None:
    """
    Don't use this directly; use torch._check_is_size instead.

    This is a softer version of _constrain_range_for_size (with min=0,
    max=Inf).  Instead of forcibly constraining a variable (and erroring if we
    failed to constrain it), it will simply advise us that a size is
    constrained in some way.  We will always defer a runtime assert for this
    constraint if we cannot prove it at compile-time, but we we only
    *sometimes* learn useful extra information at compile-time with this
    information.  This is in contrast to constrain_range_for_size, where if
    you don't call that on a fresh unbacked symint, chances are we will choke.

    TODO: Make Dynamo handle this appropriately if this is seen in Dynamo-ed
    code.  Right now this is only really used in code with AOTAutograd trace
    through, so it is not a big problem that this isn't supported, but in
    principle all of this code should be Dynamo'able too.

    TODO: I didn't support min/max because I didn't have a use case where this
    actually helped.  In principle we can support it, it just makes the
    implementation below more complicated.
    """

    # This must always succeed, because the sole allowed caller _check_is_size
    # was responsible for expect_true'ing this
    # This assert triggers expensive sym compute, do not do it until its cheap.
    # assert a >= 0

    # NB: it's important not to constrain range for size for *hinted* SymInts,
    # because it is not only unsound, it will immediately trip our asserts
    # that hints have to be consistent with static analysis!  If you somehow
    # have an unbounded SymInt that later constrains to 1, this will be
    # inconsistent with the range
    if (
        isinstance(a, SymInt)
        and isinstance(a.node, SymNode)
        and isinstance(a.node.expr, sympy.Symbol)
        and a.node.shape_env is not None
        and a.node.shape_env.is_unbacked_symint(a.node.expr)
    ):
        _constrain_range_for_size(a)

