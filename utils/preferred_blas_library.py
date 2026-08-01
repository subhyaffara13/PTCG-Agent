
def preferred_blas_library(
    backend: None | str | torch._C._BlasBackend = None,
) -> torch._C._BlasBackend:
    r"""
    Override the library PyTorch uses for BLAS operations. Choose between cuBLAS, cuBLASLt, and CK [ROCm-only].

    .. warning:: This flag is experimental and subject to change.

    When PyTorch runs a CUDA BLAS operation it defaults to cuBLAS even if both cuBLAS and cuBLASLt are available.
    For PyTorch built for ROCm, hipBLAS, hipBLASLt, and CK may offer different performance.
    This flag (a :class:`str`) allows overriding which BLAS library to use.

    * If `"cublas"` is set then cuBLAS will be used wherever possible.
    * If `"cublaslt"` is set then cuBLASLt will be used wherever possible.
    * If `"ck"` is set then CK will be used wherever possible.
    * If `"default"` (the default) is set then heuristics will be used to pick between the other options.
    * When no input is given, this function returns the currently preferred library.
    * User may use the environment variable TORCH_BLAS_PREFER_CUBLASLT=1 to set the preferred library to cuBLASLt
      globally.
      This flag only sets the initial value of the preferred library and the preferred library
      may still be overridden by this function call later in your script.

    Note: When a library is preferred other libraries may still be used if the preferred library
    doesn't implement the operation(s) called.
    This flag may achieve better performance if PyTorch's library selection is incorrect
    for your application's inputs.

    """
    if backend is None:
        pass
    elif isinstance(backend, str):
        if backend not in _BlasBackends:
            raise RuntimeError(
                f"Unknown input value. Choose from: {_BlasBackends_str}."
            )
        torch._C._set_blas_preferred_backend(_BlasBackends[backend])
    elif isinstance(backend, torch._C._BlasBackend):
        torch._C._set_blas_preferred_backend(backend)
    else:
        raise RuntimeError("Unknown input value type.")

    return torch._C._get_blas_preferred_backend()

