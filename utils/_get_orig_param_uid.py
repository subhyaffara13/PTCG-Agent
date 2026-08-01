
def _get_orig_param_uid(param: nn.Parameter) -> int:
    if not hasattr(param, "_fsdp_orig_uid"):
        uid = next(_orig_param_uid_counter)
        param._fsdp_orig_uid = uid  # pyrefly: ignore[missing-attribute]
    return param._fsdp_orig_uid  # pyrefly: ignore[missing-attribute]

