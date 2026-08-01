
def check_all_permutations(op, args, kwargs, assert_equal_fn):
    CCT, cct_mode = generate_cct_and_mode()
    expected = op(*args, **kwargs)
    for choice in generate_subclass_choices_args_kwargs(args, kwargs, CCT, cct_mode):
        new_args, new_kwargs, which_args_are_wrapped, which_kwargs_are_wrapped = choice

        try:
            actual = op(*new_args, **new_kwargs)
        # NOTE: [What errors are Composite Compliance trying to catch?]
        #
        # There's two things we want to catch:
        # - errors that would raise within the torch_dispatch impl
        # - data_ptr accesses
        # The first is easy to filter for (we could make the error a different
        # error class), the second is always going to be a RuntimeError due to
        # how it is implemented (if you try to access the data_ptr of the
        # wrapper Tensor, it raises you some internal RuntimeError).
        #
        # So the most general thing to catch here was RuntimeError. If you
        # are here and debugging why your test failed, it's plausible that
        # the operator itself is broken and that there are other tests failing.
        except RuntimeError as err:
            raise_composite_compliance_error(
                err,
                f"- wrapped_args: {which_args_are_wrapped}\n"
                f"- wrapped_kwargs: {which_kwargs_are_wrapped}\n"
            )

        def unwrap(e):
            return e.elem if isinstance(e, CCT) else e

        assert_equal_fn(tree_map(unwrap, actual), expected)

