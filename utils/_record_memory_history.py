
def _record_memory_history(
    enabled: Literal["state", "all"] | None = "all", *args, **kwargs
) -> None:
    """Enable recording of stack traces associated with memory
    allocations, so you can tell what allocated any piece of memory in
    :func:`torch.cuda.memory._snapshot()`.

    In addition to keeping stack traces with each current allocation and free,
    this will also enable recording of a history of all alloc/free events.

    Use :func:`torch.cuda.memory._snapshot()` to retrieve this information,
    and the tools in `_memory_viz.py` to visualize snapshots.

    Buffer behavior
    ---------------

    This will store up to `max_entries` instances of `TraceEntry` when enabled.
    Python trace collection defaults to `sys.maxsize`, meaning long-running
    or indefinitely running jobs should set a reasonable limit to avoid excessive
    memory use. Expect each entry to be several KB.

    Longer running workflows or those with smaller `max_entries` values will only
    store the last accumulated `max_entries` entries, meaning new entries overwrite
    older entries.

    C++ implementation for reference to ring buffer implementation:

    .. code-block:: cpp

        if (record_history) {
          if (alloc_trace->size() < alloc_trace_max_entries_) {
            alloc_trace->emplace_back(te);
          } else {
            (*alloc_trace)[alloc_trace_next++] = te;
            if (alloc_trace_next == alloc_trace_max_entries_) {
              alloc_trace_next = 0;
            }
          }
        }

    Latency impact
    --------------

    The Python trace collection is fast (2us per trace), so you may consider
    enabling this on production jobs if you anticipate ever having to debug
    memory issues.

    C++ trace collection is also fast (~50ns/frame), which for many typical programs
    works out to ~2us per trace, but can vary depending on stack depth.

    Args:
        enabled (Literal[None, "state", "all"], optional):
            `None`, disable recording memory history.
            `"state"`, keep information for currently allocated memory.
            `"all"`, additionally keep a history of all alloc/free calls.
            Defaults to "all".
        context (Literal[None, "state", "alloc", "all"], optional):
            `None`, Do not record any tracebacks.
            `"state"`, Record tracebacks for currently allocated memory.
            `"alloc"`, additionally keep tracebacks for alloc calls.
            `"all"`, additionally keep tracebacks for free calls.
            Defaults to "all".
        stacks (Literal["python", "all"], optional):
            `"python"`, include Python, TorchScript, and inductor frames in tracebacks
            `"all"`, additionally include C++ frames
            Defaults to "all".
        max_entries (int, optional): Keep a maximum of `max_entries`
            alloc/free events in the recorded history recorded.
        clear_history (bool, optional): Clear history when enabling, defaults to False.
        skip_actions (list[str], optional): List of action types to skip when recording
            memory history. This can be used to reduce memory overhead by excluding
            certain types of events from being recorded. Valid action types are:

            - `"alloc"`: Memory allocation events
            - `"free_requested"`: Free requests (memory marked for freeing)
            - `"free_completed"`: Completed free operations (memory actually freed)
            - `"segment_alloc"`: Segment allocation from cudaMalloc
            - `"segment_free"`: Segment freed back to CUDA via cudaFree
            - `"oom"`: Out-of-memory exceptions
            - `"snapshot"`: Memory snapshot generation events

            For example, to skip recording free_requested events:
            `skip_actions=["free_requested"]`

            Defaults to None (record all actions).

    """
    if isinstance(enabled, bool):
        return _record_memory_history_legacy(enabled, *args, **kwargs)
    else:
        return _record_memory_history_impl(enabled, *args, **kwargs)


def _record_memory_history(
    enabled: Literal["state", "all"] | None = "all",
    context: Literal["state", "alloc", "all"] | None = "all",
    stacks: Literal["python", "all"] = "all",
    max_entries: int = sys.maxsize,
    clear_history: bool = False,
    skip_actions: list[str] | None = None,
) -> None:
    """
    Enable recording of stack traces associated with memory allocations, so you can
    tell what allocated any piece of memory in :func:`~torch.xpu.memory._snapshot()`.

    In addition to keeping stack traces with each current allocation and free,
    this will also enable recording of a history of all alloc/free events.

    Use :func:`~torch.xpu.memory._snapshot()` to retrieve this information,
    and the tools in `_memory_viz.py` to visualize snapshots.

    Buffer behavior
    ---------------

    This will store up to `max_entries` instances of `TraceEntry` when enabled.
    Python trace collection defaults to `sys.maxsize`, meaning long-running
    or indefinitely running jobs should set a reasonable limit to avoid excessive
    memory use. Expect each entry to be several KB.

    Longer running workflows or those with smaller `max_entries` values will only
    store the last accumulated `max_entries` entries, meaning new entries overwrite
    older entries, reference to ring buffer behavior.

    Latency impact
    --------------

    The Python trace collection is fast (2us per trace), so you may consider
    enabling this on production jobs if you anticipate ever having to debug
    memory issues.

    C++ trace collection is also fast (~50ns/frame), which for many typical programs
    works out to ~2us per trace, but can vary depending on stack depth.

    Arguments:
        enabled (Literal["state", "all"], optional):
            `None`, disable recording memory history.
            `"state"`, keep information for currently allocated memory.
            `"all"`, additionally keep a history of all alloc/free calls.
            Defaults to "all".
        context (Literal["state", "alloc", "all"], optional):
            `None`, Do not record any tracebacks.
            `"state"`, Record tracebacks for currently allocated memory.
            `"alloc"`, additionally keep tracebacks for alloc calls.
            `"all"`, additionally keep tracebacks for free calls.
            Defaults to "all".
        stacks (Literal["python", "all"], optional):
            `"python"`, include Python, TorchScript, and inductor frames in tracebacks.
            `"all"`, additionally include C++ frames.
            Defaults to "all".
        max_entries (int, optional): Keep a maximum of `max_entries`
            alloc/free events in the recorded history recorded.
        clear_history (bool, optional): Clear history when enabling, defaults to ``False``.
        skip_actions (list[str], optional): List of action types to skip when recording
            memory history. This can be used to reduce memory overhead by excluding
            certain types of events from being recorded. Valid action types are:

            - `"alloc"`: Memory allocation events
            - `"free_requested"`: Free requests (memory marked for freeing)
            - `"free_completed"`: Completed free operations (memory actually freed)
            - `"segment_alloc"`: Segment allocation from SYCL runtime
            - `"segment_free"`: Segment freed back to XPU via SYCL runtime
            - `"segment_map"`: Segment map events
            - `"segment_unmap"`: Segment unmap events
            - `"snapshot"`: Memory snapshot generation events
            - `"oom"`: Out-of-memory exceptions

            For example, to skip recording free_requested events:
            `skip_actions=["free_requested"]`

            Defaults to ``None`` (record all actions).
    """
    torch._C._xpu_recordMemoryHistory(
        enabled,
        context,
        stacks,
        max_entries,
        clear_history,
        skip_actions if skip_actions is not None else [],
    )

