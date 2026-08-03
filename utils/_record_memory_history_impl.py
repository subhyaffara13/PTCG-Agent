import sys

def _record_memory_history_impl(
    enabled: str | None = "all",
    context: str | None = "all",
    stacks: str = "all",
    max_entries: int = sys.maxsize,
    device: "Device" = None,
    clear_history: bool = False,
    compile_context: bool = False,
    global_record_annotations: bool = False,
    skip_actions: list[str] | None = None,
):
    _C._cuda_record_memory_history(  # type: ignore[call-arg]
        enabled,
        context,
        stacks,
        max_entries,
        clear_history,
        compile_context,
        global_record_annotations,
        # pyrefly: ignore [bad-argument-count]
        skip_actions if skip_actions is not None else [],
    )

