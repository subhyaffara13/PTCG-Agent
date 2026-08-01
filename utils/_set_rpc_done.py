
def _set_rpc_done(ctx_id, rank_distance):
    global rpc_done
    global ctx_ids
    global known_context_ids
    rpc_done[rank_distance] = True
    ctx_ids[rank_distance] = ctx_id
    known_context_ids.add(ctx_id)

