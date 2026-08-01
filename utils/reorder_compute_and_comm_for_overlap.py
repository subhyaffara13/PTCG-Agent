
def reorder_compute_and_comm_for_overlap(
    snodes: list[BaseSchedulerNode],
) -> list[BaseSchedulerNode]:
    order = snodes
    # pyrefly: ignore [bad-assignment]
    for p in config.reorder_for_compute_comm_overlap_passes:
        if isinstance(p, str) and p in globals():
            p = globals()[p]  # it is a builtin pass
        assert callable(p), (
            f"Invalid reorder_compute_and_comm_for_overlap pass: {p} is not callable"
        )
        order = p(order)  # type: ignore[operator]
    # pyrefly: ignore [bad-return]
    return order

