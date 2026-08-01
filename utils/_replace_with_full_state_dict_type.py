
def _replace_with_full_state_dict_type(fsdp_state: _FSDPState) -> Generator:
    old_state_dict_config = fsdp_state._state_dict_config
    old_state_dict_type = fsdp_state._state_dict_type
    fsdp_state._state_dict_config = FullStateDictConfig()
    fsdp_state._state_dict_type = StateDictType.FULL_STATE_DICT
    yield
    fsdp_state._state_dict_config = old_state_dict_config
    fsdp_state._state_dict_type = old_state_dict_type

