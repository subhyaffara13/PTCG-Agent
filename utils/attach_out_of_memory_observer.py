from typing import Callable

def attach_out_of_memory_observer(
    observer: Callable[[int, int, int, int], None],
) -> None:
    r"""Attach an out-of-memory observer to MTIA memory allocator"""
    torch._C._mtia_attachOutOfMemoryObserver(observer)

