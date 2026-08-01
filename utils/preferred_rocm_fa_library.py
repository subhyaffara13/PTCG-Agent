
def preferred_rocm_fa_library(
    backend: None | str | torch._C._ROCmFABackend = None,
) -> torch._C._ROCmFABackend:
    r"""
    [ROCm-only]
    Override the backend PyTorch uses in ROCm environments for Flash Attention. Choose between AOTriton and CK

    .. warning:: This flag is experimental and subject to change.

    When Flash Attention is enabled and desired, PyTorch defaults to using AOTriton as the backend.
    This flag (a :class:`str`) allows users to override this backend to use composable_kernel

    * If `"default"` is set then the default backend will be used wherever possible. Currently AOTriton.
    * If `"aotriton"` is set then AOTriton will be used wherever possible.
    * If `"ck"` is set then CK will be used wherever possible.
    * When no input is given, this function returns the currently preferred library.
    * User may use the environment variable TORCH_ROCM_FA_PREFER_CK=1 to set the preferred library to CK
      globally.

    Note: When a library is preferred other libraries may still be used if the preferred library
    doesn't implement the operation(s) called.
    This flag may achieve better performance if PyTorch's library selection is incorrect
    for your application's inputs.
    """
    if backend is None:
        pass
    elif isinstance(backend, str):
        if backend not in _ROCmFABackends:
            raise RuntimeError(
                f"Unknown input value. Choose from: {_ROCmFABackends_str}."
            )
        torch._C._set_rocm_fa_preferred_backend(_ROCmFABackends[backend])
    elif isinstance(backend, torch._C._ROCmFABackend):
        torch._C._set_rocm_fa_preferred_backend(backend)
    else:
        raise ValueError(f"Unknown input value. Choose from: {_ROCmFABackends_str}.")

    return torch._C._get_rocm_fa_preferred_backend()

