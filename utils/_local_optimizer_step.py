
def _local_optimizer_step(local_optim_rref, autograd_ctx_id):
    local_optim = local_optim_rref.local_value()
    local_optim.step(autograd_ctx_id)

