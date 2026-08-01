
def x86_isa_checker() -> list[str]:
    supported_isa: list[str] = []

    def _check_and_append_supported_isa(
        dest: list[str], isa_supported: bool, isa_name: str
    ) -> None:
        if isa_supported:
            dest.append(isa_name)

    Arch = platform.machine()
    """
    Arch value is x86_64 on Linux, and the value is AMD64 on Windows.
    """
    if Arch != "x86_64" and Arch != "AMD64":
        return supported_isa

    avx2 = torch.cpu._is_avx2_supported()
    avx512 = torch.cpu._is_avx512_supported()
    avx512_vnni = avx512 and torch.cpu._is_vnni_supported()
    amx_tile = torch.cpu._is_amx_tile_supported()

    _check_and_append_supported_isa(supported_isa, avx2, "avx2")
    _check_and_append_supported_isa(supported_isa, avx512, "avx512")
    _check_and_append_supported_isa(supported_isa, avx512_vnni, "avx512_vnni")
    _check_and_append_supported_isa(supported_isa, amx_tile, "amx_tile")

    return supported_isa

