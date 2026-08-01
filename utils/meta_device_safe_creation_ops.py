
def meta_device_safe_creation_ops():
    """
    During meta-device model initialisation, ``torch.linspace`` produces meta
    tensors that have no data.  Custom models loaded from the Hub (remote code)
    often call ``.item()`` on these tensors to compute scalar hyperparameters
    (e.g. stochastic-depth / drop-path schedules).  Native transformers models
    already pass ``device="cpu"`` explicitly for such calls (see e.g.
    ``modeling_swin.py``, ``modeling_pvt_v2.py``), but remote-code models
    written before v5 do not.

    This context manager patches ``torch.linspace`` to default to
    ``device="cpu"`` when no explicit device is requested, matching the best
    practice already used throughout transformers.  Calls that supply an
    explicit ``device`` argument (e.g. ``device=self.logits.device``) are left
    untouched.  ``torch.arange`` is intentionally NOT patched because it is
    used in RoPE computations where the device must match model parameters.
    """
    original_linspace = torch.linspace

    def _safe_linspace(*args, **kwargs):
        kwargs.setdefault("device", "cpu")
        return original_linspace(*args, **kwargs)

    torch.linspace = _safe_linspace
    try:
        yield
    finally:
        torch.linspace = original_linspace

