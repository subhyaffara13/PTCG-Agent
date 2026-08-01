
def snapshot_verbose_logging_enabled() -> bool:
    return torch._logging._internal.log_state.is_artifact_enabled(
        "compiled_autograd_verbose"
    )

