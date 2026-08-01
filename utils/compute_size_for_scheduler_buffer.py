
def compute_size_for_scheduler_buffer(
    name_to_buf: dict[str, SchedulerBuffer],
) -> dict[str, tuple[int, int]]:
    """
    Compute the size of each scheduler buffer, including (1) memory allocated when
    it is created and (2) memory deallocated when it is freed.

    We specially handle the case of MultiOutputLayout.
    Consider the following case:
        buf0 = some_ops_with_multi_outputs(...)
        buf1 = buf0[0] # assume 10 bytes
        buf2 = buf0[1] # assume 20 bytes
    In such cases,
        buf0: at creation, 30 bytes allocated, when deleted, 0 bytes freed
        buf1: at creation, 0 bytes allocated, when deleted, 10 bytes freed
        buf2: at creation, 0 bytes allocated, when deleted, 20 bytes freed

    When an operation mutates a buffer in-place, the scheduler creates a new buffer name
    to track the "before" and "after" states, even though they share the same memory.

    The mutated buffer represents a rename with zero allocation and deallocation cost.
    During dependency tracking, we transfer dependencies from the mutated name back to
    the original buffer, ensuring the original memory is only freed when all aliases
    are done.

    This handles cases where a buffer has multiple non-overlapping aliases - rather than
    trying to assign free costs to individual aliases, we forward all alias dependencies
    to the original buffer.

    Consider:
        buf0 = op0()
        buf1 = mutation_op_(buf0)
        del buf0
        ...
        op(buf1)
        del buf1

    The only memory events are the creation prior to op0, and the deletion following buf1.

    Returns:
        A dictionary mapping a scheduler buffer to a tuple of (size_alloc, size_free).
    """
    from .ir import MultiOutput
    from .scheduler import OutputNode

    sched_buf_to_size: dict[str, tuple[int, int]] = dict()

    def _compute_and_update_buf_size(
        sched_buf: SchedulerBuffer, user_of_MultiOutputLayout: bool = False
    ) -> int:
        if sched_buf.get_name() in V.graph.scheduler.mutation_real_name:
            sched_buf_to_size[sched_buf.get_name()] = (0, 0)
            return 0
        elif isinstance(sched_buf.node.layout, NoneLayout):
            sched_buf_to_size[sched_buf.get_name()] = (0, 0)
            return 0
        elif isinstance(sched_buf.node.layout, MultiOutputLayout):
            size_alloc = 0
            for user in sched_buf.users:
                if isinstance(user.node, OutputNode):
                    continue
                for buf in user.node.get_outputs():
                    if isinstance(buf.node, MultiOutput):
                        size_alloc += _compute_and_update_buf_size(buf, True)
            sched_buf_to_size[sched_buf.get_name()] = (
                0 if user_of_MultiOutputLayout else size_alloc,
                0,
            )
            return size_alloc
        else:
            buf_size = V.graph.sizevars.optimization_hint(
                sched_buf.node.get_numel(), fallback=0
            ) * get_dtype_size(sched_buf.node.get_dtype())
            sched_buf_to_size[sched_buf.get_name()] = (
                0 if user_of_MultiOutputLayout else buf_size,
                buf_size,
            )
            return buf_size

    for sched_buf in name_to_buf.values():
        # skip if sched_buf is already processed as an user of another SchedulerBuffer
        # whose layout is of the type MultiOutputLayout
        if sched_buf.get_name() not in sched_buf_to_size:
            _compute_and_update_buf_size(sched_buf)

    return sched_buf_to_size

