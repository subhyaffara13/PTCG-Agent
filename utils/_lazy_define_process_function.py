
def _lazy_define_process_function(flash_function):
    """
    Depending on the version and kernel some features are not supported. Due to limitations in
    `torch.compile`, we opt to statically type which (optional) kwarg parameters are supported
    within `_process_flash_attention_kwargs`.

    NOTE: While all supported kwargs are marked as `True`, everything else is marked as `False`.
          This might be confusing for kwargs that we use in any case, e.g. `is_causal`.
    """

    flash_parameters = inspect.signature(flash_function).parameters
    process_parameters = inspect.signature(_process_flash_attention_kwargs).parameters

    supports_mapping = {}
    for param in process_parameters:
        fa_param = _hf_api_to_flash_mapping.get(param, param)
        supports_mapping[fa_param] = fa_param in flash_parameters

        if (fa_alternative_name := _flash_api_alternative_names.get(param, param)) != fa_param:
            supports_mapping[fa_alternative_name] = fa_alternative_name in flash_parameters

    return partial(_process_flash_attention_kwargs, supports_mapping=supports_mapping)

