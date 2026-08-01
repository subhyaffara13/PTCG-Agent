
def _needs_obs_or_fq(
    prev_output_dtype: Any,
    prev_output_is_dynamic: bool,
    cur_target_dtype: Any,
    cur_target_is_dynamic: bool,
    reuse_input_obs_or_fq: bool,
    is_zeroth_arg: bool = False,
) -> bool:
    """
    note: we will treat "not specified" as torch.float for now
    utility function that checks if we should insert an observer or fake quant node
    base on the requested dtype for the nodes from user

    is_zeroth_arg: we only dynamically quantize the first arg of the node right now
      this should be removed when we enable configuring dynamic quantization
      for a specific argument, this can be removed if we deprecate fx graph mode
      quantization

    """

    # need to insert placeholder observer for dynamic quantization so that it can
    # be converted to choose_qparams -> q -> dq in convert step
    if cur_target_is_dynamic:
        if cur_target_dtype not in _OBS_DTYPE_LIST:
            raise AssertionError(
                f"Expected cur_target_dtype to be torch.float, but got: {cur_target_dtype}"
            )
        if prev_output_dtype in _DO_NOT_OBS_DTYPE_LIST:
            raise AssertionError(
                "prev_output_dtype must not be in _DO_NOT_OBS_DTYPE_LIST"
            )
        return is_zeroth_arg
    if reuse_input_obs_or_fq:
        return False
    # non dynamic quantization
    if cur_target_dtype in _OBS_DTYPE_LIST:
        return (
            prev_output_dtype in _OBS_DTYPE_LIST + [torch.float]
            and cur_target_dtype != prev_output_dtype
        )

    # lots of error checking are skipped here for now
    return False

