
def _log_torch_version() -> None:
    import torch
    from torch._environment import is_fbcode
    from torch._utils_internal import get_torch_source_version

    version_info: dict[str, object] = {
        "pytorch_version": torch.__version__,
        "commit": get_torch_source_version(),
        "oss": not is_fbcode(),
    }

    trace_structured(
        "artifact",
        metadata_fn=lambda: {"name": "torch_version", "encoding": "json"},
        payload_fn=lambda: version_info,
        suppress_context=True,
        expect_trace_id=False,
    )

