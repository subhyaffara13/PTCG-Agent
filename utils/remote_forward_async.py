
def remote_forward_async(remote_module, args):
    # Since future cannot be pickled and sent over the RPC layer,
    # have to wait and behave just like ``forward_sync``.
    return remote_module.forward_async(*args).wait()

