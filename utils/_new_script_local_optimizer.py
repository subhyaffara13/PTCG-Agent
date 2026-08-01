
def _new_script_local_optimizer(optim_cls, local_params_rref, *args, **kwargs):
    optim = _ScriptLocalOptimizer(optim_cls, local_params_rref, *args, **kwargs)

    with _ScriptLocalOptimizer.compile_lock:
        script_optim = jit.script(optim)
        return rpc.RRef(script_optim, _ScriptLocalOptimizerInterface)

