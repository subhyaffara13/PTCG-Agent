
def get_state_ir_cache_name(state: State) -> str:
    return get_ir_cache_name(state.id, state.xpath, state.options)

