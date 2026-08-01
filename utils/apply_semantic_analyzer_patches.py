
def apply_semantic_analyzer_patches(patches: list[tuple[int, Callable[[], None]]]) -> None:
    """Call patch callbacks in the right order.

    This should happen after semantic analyzer pass 3.
    """
    patches_by_priority = sorted(patches, key=lambda x: x[0])
    for priority, patch_func in patches_by_priority:
        patch_func()

