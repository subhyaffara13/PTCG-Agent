
def _hide_source_ranges() -> Iterator[None]:
    old_enable_source_ranges = torch._C.Graph.global_print_source_ranges  # type: ignore[attr-defined]
    try:
        torch._C.Graph.set_global_print_source_ranges(False)  # type: ignore[attr-defined]
        yield
    finally:
        torch._C.Graph.set_global_print_source_ranges(old_enable_source_ranges)  # type: ignore[attr-defined]

