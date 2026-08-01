
def _get_flex_flash_fwd_configs(
    has_score_mod: bool,
    has_aux_tensors: bool,
) -> list[FlexFlashConfig]:
    if not has_score_mod or not torch._inductor.config.max_autotune:
        return [FlexFlashConfig()]
    if has_aux_tensors:
        return [FlexFlashConfig(score_mod_vec_size=1)]
    return [
        FlexFlashConfig(score_mod_vec_size=v) for v in (1, 2, 4, 8, 16, 32, 64, 128)
    ]

