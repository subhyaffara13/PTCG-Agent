
def is_torchaudio_available() -> bool:
    return is_torch_available() and _is_package_available("torchaudio")[0]

