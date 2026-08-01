
def check_with_mode(op, args, kwargs, assert_equal_fn):
    CCT, cct_mode = generate_cct_and_mode()

    def wrap(e):
        return CCT(e, cct_mode) if isinstance(e, torch.Tensor) else e

    expected = op(*args, **kwargs)

    args = tree_map(wrap, args)
    kwargs = tree_map(wrap, kwargs)
    try:
        with cct_mode:
            actual = op(*args, **kwargs)
    # see NOTE: [What errors are Composite Compliance trying to catch?]
    except RuntimeError as err:
        raise_composite_compliance_error(err)

    def unwrap(e):
        return e.elem if isinstance(e, CCT) else e

    assert_equal_fn(tree_map(unwrap, actual), expected)

