
def _check_capability():
    if torch.version.cuda is None:  # on ROCm we don't want this check
        return

    arch_list = get_arch_list()
    if len(arch_list) == 0:
        return

    code_ccs = [_extract_arch_version(cc) for cc in arch_list]
    for d in range(device_count()):
        major, minor = get_device_capability(d)
        device_cc = 10 * major + minor
        if not any(
            _code_compatible_with_device(device_cc, code_cc) for code_cc in code_ccs
        ):
            _warn_unsupported_code(d, device_cc, code_ccs)

