
def _run_trainer_torchscript(rref_t1, t2, ps, rank_diff, sparse):
    with dist_autograd.context() as context_id:
        ret = rpc.rpc_sync(ps, my_script_ref_add, args=(rref_t1, t2))
        if sparse:
            loss = torch.sparse.sum(ret)
        else:
            loss = ret.sum()
        dist_autograd.backward(context_id, [loss])
        # prevent deleting dist autograd context
        rpc.rpc_sync(ps, _set_rpc_done, args=(context_id, rank_diff))
        rpc.rpc_sync(ps, _check_rpc_done, args=(0,))

