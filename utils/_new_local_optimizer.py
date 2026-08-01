
def _new_local_optimizer(optim_cls, local_params_rref, *args, **kwargs):
    return rpc.RRef(_LocalOptimizer(optim_cls, local_params_rref, *args, **kwargs))

