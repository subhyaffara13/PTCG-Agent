
def create_warmup_future_states(
    num: int,
    status: RequestStatus,
    num_q_tokens: int,
    max_kv_read: int,
    cache: Any,  # not annotated to avoid circular import
) -> list[FutureRequestState]:
    """A utility function to create a list of FutureRequestStates for the warmup of CB."""
    # Setup
    request_ids = [f"__warmup_{status.name}_{i}__" for i in range(num)]
    total_tokens = num_q_tokens + max_kv_read
    blocks_needed = ceil(total_tokens / cache.block_size)
    # Main loop
    future_states = []
    for req_id in request_ids:
        state = RequestState(request_id=req_id, initial_tokens=[0] * total_tokens, max_new_tokens=1)
        state._status = status  # bypass the property setter to avoid the lifecycle side effects
        state.tokens_to_process = [0] * num_q_tokens
        state.position_offset = max_kv_read
        # Stop if allocation fails for any request
        allocated = cache.allocate_blocks(blocks_needed, state.request_id, 0)
        if allocated is None:
            return future_states
        future_states.append(
            FutureRequestState(state, has_new_token=True, complete_blocks=0, query_length=num_q_tokens)
        )
    return future_states

