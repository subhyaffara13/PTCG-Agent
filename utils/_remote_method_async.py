
def _remote_method_async(method, rref, *args, **kwargs):
    args_tup = tuple([method, rref] + list(args))
    return rpc.rpc_async(rref.owner(), _call_method, args=args_tup, kwargs=kwargs)

