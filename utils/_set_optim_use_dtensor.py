
def _set_optim_use_dtensor(
    fsdp_state: _FSDPState,
    state_dict_settings: StateDictSettings,
) -> None:
    # If device_mesh is passed in when initializing FSDP, we automatically turn the
    # _use_dtensor flag to be true for ShardedOptimStateDictConfig() if state_dict_type
    # has to be set to SHARDED_STATE_DICT.
    if getattr(fsdp_state, "_device_mesh", None):
        state_dict_type = state_dict_settings.state_dict_type
        if state_dict_type == StateDictType.LOCAL_STATE_DICT:
            raise RuntimeError(
                "Found state_dict_type LOCAL_STATE_DICT. "
                "DeviceMesh is not compatible with LOCAL_STATE_DICT. "
                "Please set state_dict_type to SHARDED_STATE_DICT to get DTensor state_dict."
            )
        else:
            state_dict_settings.optim_state_dict_config._use_dtensor = True

