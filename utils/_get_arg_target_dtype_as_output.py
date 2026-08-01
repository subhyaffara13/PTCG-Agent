
def _get_arg_target_dtype_as_output(
    arg: Node,
    named_modules: dict[str, torch.nn.Module],
    obs_or_fq_map: dict[EdgeOrNode, ObserverOrFakeQuantize],
    is_qat: bool,
) -> torch.dtype | None:
    arg_as_output_act_obs_or_fq = _get_output_act_obs_or_fq(
        arg, named_modules, obs_or_fq_map, is_qat
    )
    arg_as_output_target_dtype, _ = _get_dtype_and_is_dynamic(
        arg_as_output_act_obs_or_fq
    )
    return arg_as_output_target_dtype

