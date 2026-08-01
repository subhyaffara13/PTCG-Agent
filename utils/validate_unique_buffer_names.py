
def validate_unique_buffer_names(
    nodes: list[BaseSchedulerNode],
    name_to_buf: dict[str, SchedulerBuffer],
    name_to_freeable_input_buf: dict[str, FreeableInputBuffer],
) -> None:
    """
    Validate that for each node's output buffer, the name_to_buf mapping is correct.
    For each output buffer buf, we should have name_to_buf[buf.get_name()] == buf.
    Also validate that no buffer names overlap with freeable input buffer names.

    Raises:
        RuntimeError: If buffer name mapping is incorrect or names overlap
    """
    for node in nodes:
        for buf in node.get_outputs():
            buf_name = buf.get_name()

            # Check if buffer name exists in the mapping
            if buf_name not in name_to_buf:
                raise RuntimeError(
                    f"{buf_name} from {node.get_name()} is not found in name_to_buf mapping."
                    f" This indicates a missing buffer mapping."
                )

            # Check if the mapping points to the correct buffer object
            if name_to_buf[buf_name] != buf:
                raise RuntimeError(
                    f"Buffer name mapping is incorrect for '{buf_name}'."
                    f"Expected name_to_buf['{buf_name}'] to be {buf.debug_str()}"
                    f"but got {name_to_buf[buf_name].debug_str()}"
                    f"This indicates some buffers share the same name"
                )

            # Check if buffer name conflicts with freeable input buffer names
            if buf_name in name_to_freeable_input_buf:
                raise RuntimeError(
                    f"Buffer name conflict detected: '{buf_name}' from node {node.get_name()} "
                    f"is also used as a freeable input buffer name. "
                )

