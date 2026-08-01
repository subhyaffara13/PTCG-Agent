
def _check_is_size(i, message=None, *, max=None):
    """Checks that a given integer is a valid size (i.e., is non-negative).
    You should use this over ``_check(i >= 0)`` because it can prevent
    ``GuardOnDataDependentSymNode`` exceptions by opting yourself into alternate
    semantics for ``guard_size_oblivious`` tests that treat values 0 and 1
    equivalently to all other values.

    When max is not None, this specifies an upper bound equivalent to
    ``_check(i <= max)``.  This bound is also subject to alternate semantics:
    in ``guard_size_oblivious`` tests, we assume that a constant max bound is
    treated equivalently to all other values.  Symbolic max bounds are not yet
    supported.

    NB: Do NOT use this in contexts where a -1 size would be valid (indicating
    to infer the size from context, or if you should wrap-around or truncate).
    Only use this if the only valid value is an honest to goodness size.
    """
    # This is responsible for the expect_true
    _check(i >= 0, message)
    from torch.fx.experimental.symbolic_shapes import _advise_is_size

    _advise_is_size(i)

    if max is not None:
        _check(i <= max, message)

        from torch.fx.experimental.symbolic_shapes import _advise_is_bounded

        _advise_is_bounded(i, max)

