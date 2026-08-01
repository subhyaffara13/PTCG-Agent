
def _resolve_backend(backend: str | None, use_fast: bool | None, base_class_name: str | None) -> str:
    """Resolve raw backend inputs to a concrete backend name ('torchvision' or 'pil').

    Handles, in order:
    - Deprecated ``use_fast`` flag: warns and converts to an explicit backend string when no
      explicit backend is given.
    - Explicit backend string: returned as-is.
    - None resolution: forces 'pil' for processors in DEFAULT_TO_PIL_BACKEND_IMAGE_PROCESSORS
      (Lanczos interpolation, unsupported by torchvision < 0.27); otherwise picks 'torchvision'
      when available, falling back to 'pil'.
    """
    if use_fast is not None:
        logger.warning_once(
            "The `use_fast` parameter is deprecated and will be removed in a future version. "
            'Use `backend="torchvision"` instead of `use_fast=True`, or `backend="pil"` instead of `use_fast=False`.'
        )
        if backend is None:
            backend = "torchvision" if use_fast else "pil"

    if backend is None:
        if base_class_name in DEFAULT_TO_PIL_BACKEND_IMAGE_PROCESSORS:
            return "pil"
        return "torchvision" if is_torchvision_available() else "pil"

    return backend

