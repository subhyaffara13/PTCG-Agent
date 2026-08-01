
def _script_local_optimizer_step(
    local_optim_rref: RRef[_ScriptLocalOptimizerInterface], autograd_ctx_id: int
) -> None:
    local_optim = local_optim_rref.local_value()
    local_optim.step(autograd_ctx_id)

