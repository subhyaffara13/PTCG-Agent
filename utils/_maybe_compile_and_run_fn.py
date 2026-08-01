
def _maybe_compile_and_run_fn(fn, *args):
    if not torch.compiler.is_dynamo_compiling():
        return _hop_compile_and_call(fn, args)
    else:
        return fn(*args)

