
def check_torch_load_is_safe() -> None:
    if not is_torch_greater_or_equal("2.6"):
        raise ValueError(
            "Due to a serious vulnerability issue in `torch.load`, even with `weights_only=True`, we now require users "
            "to upgrade torch to at least v2.6 in order to use the function. This version restriction does not apply "
            "when loading files with safetensors."
            "\nSee the vulnerability report here https://nvd.nist.gov/vuln/detail/CVE-2025-32434"
        )

