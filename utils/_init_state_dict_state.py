
def _init_state_dict_state(state: _FSDPState) -> _FSDPState:
    state._state_dict_type = StateDictType.FULL_STATE_DICT
    state_dict_config: StateDictConfig = FullStateDictConfig()
    state._optim_state_dict_config = FullOptimStateDictConfig()
    state._state_dict_config = state_dict_config
    unshard_params_ctx: dict[nn.Module, Generator] = {}
    state._unshard_params_ctx = unshard_params_ctx

    return state

