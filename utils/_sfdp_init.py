
def _sfdp_init(input_device: torch.device | None = None):
    for key, register_replacement_kwargs in _get_sfdp_patterns(input_device):
        gen_register_replacement(key, **register_replacement_kwargs)

