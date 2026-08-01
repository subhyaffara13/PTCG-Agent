
def _get_cat_config(dtype_configs: list[DTypeConfig]) -> BackendPatternConfig:
    return (
        BackendPatternConfig(torch.cat)
        .set_observation_type(ObservationType.OUTPUT_SHARE_OBSERVER_WITH_INPUT)
        .set_dtype_configs(dtype_configs)
    )

