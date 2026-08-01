
def _assert_scalar(data, msg):
    # NB: These will be handled at codegen time
    # Not sure if we are guaranteed to be able to serve out truth from the
    # deferred_runtime_asserts, TODO: try this assert out
    # See [NOTE] Codegen runtime asserts in Inductor
    # assert bool(data.scalar), data
    return None

