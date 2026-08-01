
def make_fx_check(
    func,
    args,
    kwargs,
    tracing_mode,
    assert_close=torch.testing.assert_close,
    randomize_data=False,
):
    f, *new_args = handle_sizes_for_dynamic_shapes(func, args, kwargs)

    def run(f, *args, **kwargs):
        return wrapper_set_seed(f, *args, **kwargs)

    traced_f = make_fx(f, tracing_mode=tracing_mode)(*new_args)

    msg = (
        "op(*args, **kwargs) and make_fx(op)(*args, **kwargs) produced different "
        "values. This could mean that your abstract impls (meta/FakeTensor impls) "
        "are incorrect, that your operator is not completely traceable (e.g., "
        "it relies on some global state), or that there is a bug in make_fx. "
        "Note that if you passed a python function (and not an operator) to "
        "make_fx_check, it is still possible that the python function will still "
        "work with torch.compile because it handles capturing pieces of "
        "your python code to compile."
    )

    # Randomize the data and run the traced graph with it, to catch bugs
    # where we may have baked in Tensor data into the trace.
    # This is not guaranteed to succeed, because `f` might have preconditions
    # on the values of the inputs, so we just ignore if we used
    # random data and it fails.
    if randomize_data:
        new_args = randomize(new_args)
    try:
        expected = run(f, *new_args)
    except Exception:
        if randomize_data:
            return
        raise
    result = run(traced_f, *new_args)
    assert_close(result, expected, msg=msg)

