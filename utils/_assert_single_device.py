
def _assert_single_device(device: torch.device, context: str) -> None:
    """Reject DeepGEMM calls that span multiple CUDA devices in the same process
    (e.g. ``device_map="auto"`` across N GPUs). DeepGEMM loads each kernel via
    ``cuKernelGetFunction``, which binds the resulting ``CUfunction`` handle to
    the CUDA context that was current at load time. Driving the same cached
    handle from a different device's context launches it against the wrong
    module/context and produces garbage. Distributed setups (torchrun + TP/EP)
    don't trip this because each process owns exactly one device's context.

    The fix is a build-time choice on the DeepGEMM side: compiling with
    ``DG_JIT_USE_RUNTIME_API=1`` swaps the loader for the runtime API
    (context-free ``cudaKernel_t``) and lifts the restriction — but it has to
    be baked into the wheel, setting the env var at Python runtime won't change
    the loader the cached ``.so`` already uses. Until the kernels-community build
    we ship picks that up, we reject single-process multi-device by default.

    Raised as :class:`ImportError` from the per-linear path so :func:`fp8_linear`
    falls back to Triton (which loads through the runtime API and has no such
    binding); raised as :class:`RuntimeError` from the experts path where there's
    no fallback — the user explicitly chose ``experts_implementation="deepgemm"``
    and must switch to ``"grouped_mm"`` / ``"eager"`` or run distributed.
    """
    idx = device.index if device.index is not None else torch.cuda.current_device()
    _DEEPGEMM_VISITED_DEVICES.add(idx)
    if len(_DEEPGEMM_VISITED_DEVICES) <= 1:
        return
    msg = (
        "DeepGEMM caches each kernel's `CUfunction` against the CUDA context it was first "
        "loaded under, so driving it from a different device in the same process produces "
        "garbage. Run distributed (TP/EP) so each process owns one device, "
    )
    if context == "linear":
        raise ImportError(msg + "or fall back to the Triton kernel (handled automatically).")
    raise RuntimeError(msg + "or pick `experts_implementation='grouped_mm'`.")

