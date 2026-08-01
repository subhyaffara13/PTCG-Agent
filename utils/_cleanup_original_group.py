
def _cleanup_original_group(target_pg: ProcessGroup, is_default_group: bool) -> None:
    """Clean up the original process group safely."""
    try:
        destroy_process_group(target_pg)
    except Exception:
        group_type = "default" if is_default_group else "non-default"
        logger.warning(
            "Failed to destroy %s group during shrinking", group_type, exc_info=True
        )

    # Ensure global state cleanup even if destroy_process_group fails
    _cleanup_process_group_global_state(target_pg)

