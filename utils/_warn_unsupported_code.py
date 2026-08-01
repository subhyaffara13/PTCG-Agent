
def _warn_unsupported_code(device_index: int, device_cc: int, code_ccs: list[int]):
    name = get_device_name(device_index)

    compatible_releases: list[str] = []
    for cuda, build_ccs in PYTORCH_RELEASES_CODE_CC.items():
        if any(_code_compatible_with_device(device_cc, cc) for cc in build_ccs):
            compatible_releases.append(cuda)

    lines = [
        f"Found GPU{device_index} {name} which is of compute capability (CC) {device_cc // 10}.{device_cc % 10}.",
        "The following list shows the CCs this version of PyTorch was built for and the hardware CCs it supports:",
    ] + [
        f"- {cc // 10}.{cc % 10} which supports hardware CC {DEVICE_REQUIREMENT[cc]}"
        for cc in code_ccs
    ]

    if len(compatible_releases) > 0:
        releases_str = ", ".join(compatible_releases)
        lines.append(
            "Please follow the instructions at https://pytorch.org/get-started/locally/ to "
            + f"install a PyTorch release that supports one of these CUDA versions: {releases_str}"
        )

    warnings.warn("\n".join(lines), stacklevel=2)

