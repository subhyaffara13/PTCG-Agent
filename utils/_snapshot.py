
def _snapshot(device: "Device" = None, augment_with_fx_traces=False):
    """Save a snapshot of CUDA memory state at the time it was called.

    The state is represented as a dictionary with the following structure.

    .. code-block:: python

        class Snapshot(TypedDict):
            segments: List[Segment]
            device_traces: List[List[TraceEntry]]


        class Segment(TypedDict):
            # Segments are memory returned from a cudaMalloc call.
            # The size of reserved memory is the sum of all Segments.
            # Segments are cached and reused for future allocations.
            # If the reuse is smaller than the segment, the segment
            # is split into more then one Block.
            # empty_cache() frees Segments that are entirely inactive.
            address: int
            total_size: int  #  cudaMalloc'd size of segment
            stream: int
            segment_type: Literal["small", "large"]  # 'large' (>1MB)
            segment_pool_id: Tuple[
                int, int
            ]  # id of the memory pool owning this segment
            allocated_size: int  # size of memory in use
            active_size: int  # size of memory in use or in active_awaiting_free state
            blocks: List[Block]


        class Block(TypedDict):
            # A piece of memory returned from the allocator, or
            # current cached but inactive.
            size: int
            requested_size: int  # size requested during malloc, may be smaller than
            # size due to rounding
            address: int
            state: Literal[
                "active_allocated",  # used by a tensor
                "active_awaiting_free",  # waiting for another stream to finish using
                # this, then it will become free
                "inactive",
            ]  # free for reuse
            frames: List[Frame]  # stack trace from where the allocation occurred


        class Frame(TypedDict):
            filename: str
            line: int
            name: str
            # Optional FX debug fields (present when augment_with_fx_traces=True
            # and the frame corresponds to FX-generated code)
            fx_node_op: str  # FX node operation type (e.g., 'call_function', 'output')
            fx_node_name: str  # FX node name (e.g., 'linear', 'relu_1')
            fx_original_trace: str  # Original model source code stack trace


        class TraceEntry(TypedDict):
            # When `torch.cuda.memory._record_memory_history()` is enabled,
            # the snapshot will contain TraceEntry objects that record each
            # action the allocator took.
            action: Literal[
                "alloc"  # memory allocated
                "free_requested",  # the allocated received a call to free memory
                "free_completed",  # the memory that was requested to be freed is now
                # able to be used in future allocation calls
                "segment_alloc",  # the caching allocator ask cudaMalloc for more memory
                # and added it as a segment in its cache
                "segment_free",  # the caching allocator called cudaFree to return memory
                # to cuda possibly trying free up memory to
                # allocate more segments or because empty_caches was called
                "oom",  # the allocator threw an OOM exception. 'size' is
                # the requested number of bytes that did not succeed
                "snapshot",  # the allocator generated a memory snapshot
                # useful to coorelate a previously taken
                # snapshot with this trace
            ]
            addr: int  # not present for OOM
            frames: List[Frame]
            size: int
            stream: int
            device_free: int  # only present for OOM, the amount of
            # memory cuda still reports to be free
            pool_id: Tuple[int, int]  # id of the memory pool for this entry

    Args:
        device: Device to capture snapshot for. If None, captures for current device.
        augment_with_fx_traces: If True, augment stack trace frames with FX debug information
                                that maps generated FX code back to original model source code.
                                This adds fx_node_op, fx_node_name, fx_original_trace, and
                                fx_node_info fields to Frame objects. Default: False.

    Returns:
        The Snapshot dictionary object
    """
    s = _C._cuda_memorySnapshot(None)
    if augment_with_fx_traces:
        s = _augment_memory_snapshot_stack_traces(s)  # type: ignore[assignment, arg-type]
    return s


def _snapshot(device: Device = None, augment_with_fx_traces: bool = False):
    """
    Capture a snapshot of the XPU memory state at the time this function is called.

    The returned snapshot is a dictionary with the following structure.

    .. code-block:: python

        class Snapshot(TypedDict):
            segments: List[Segment]
            device_traces: List[List[TraceEntry]]


        class Segment(TypedDict):
            # A Segment represents a contiguous memory region returned by the SYCL runtime.
            #
            # All reserved memory is composed of these segments. Segments are
            # cached and reused by the allocator. When allocations are smaller
            # than the segment, the segment may be split into multiple Blocks.
            #
            # Calling :func:`~torch.xpu.memory.empty_cache` releases segments that are entirely inactive.
            address: int
            total_size: int  #  total size of segment
            stream: int
            segment_type: Literal["small", "large"]  # 'large' (>1MB)
            allocated_size: int  # size of memory in use
            active_size: int  # size of memory in use or in active_awaiting_free state
            blocks: List[Block]


        class Block(TypedDict):
            # A sub-region of a Segment, either currently allocated or cached for reuse.
            size: int
            requested_size: int  # Original requested size (may be smaller than `size`)
            address: int
            state: Literal[
                "active_allocated",  # used by a tensor
                "active_awaiting_free",  # waiting for another stream synchronization, then become free
                "inactive",  # free for reuse
            ]
            frames: List[Frame]  # stack trace from where the allocation occurred


        class Frame(TypedDict):
            filename: str
            line: int
            name: str
            # Optional fields when `augment_with_fx_traces=True` and the frame
            # corresponds to FX-generated code.
            fx_node_op: str  # FX node operation type (e.g., 'call_function', 'output')
            fx_node_name: str  # FX node name (e.g., 'linear', 'relu_1')
            fx_original_trace: str  # Original model source code stack trace


        class TraceEntry(TypedDict):
            # Trace entries are recorded only when :func:`~torch.xpu.memory._record_memory_history` is enabled.
            action: Literal[
                "alloc"  # memory allocated
                "free_requested",  # received a call to free memory
                "free_completed",  # memory reclaimed and reusable
                "segment_alloc",  # ask SYCL runtime for more memory
                "segment_free",  # called SYCL runtime to return memory to XPU
                "segment_map",  # ask SYCL runtime to map memory
                "segment_unmap",  # called SYCL runtime to unmap memory
                "snapshot",  # snapshot taken
                "oom",  # threw an OOM exception
            ]
            addr: int  # not present for OOM
            frames: List[Frame]
            size: int
            stream: int
            device_free: int  # only present for OOM, the amount of free memory reported by the device

    Arguments:
        device (torch.device or int or str, optional): selected device. It uses the current device,
            given by :func:`~torch.xpu.current_device`, if :attr:`device` is ``None`` (default).
        augment_with_fx_traces (bool, optional): If True, augment stack trace frames with FX debug information
            that maps generated FX code back to original model source code. This adds the FX-related
            fields (fx_node_op, fx_node_name, fx_original_trace) to Frame objects. Default is ``False``.

    Returns:
        The Snapshot dictionary object
    """
    s = torch._C._xpu_memorySnapshot(None)
    if augment_with_fx_traces:
        s = _augment_memory_snapshot_stack_traces(s)  # type: ignore[assignment, arg-type]
    return s

