
def _run_fn_with_dynamo_disabled(fn, *args, **kwargs):
    return fn(*args, **kwargs)

