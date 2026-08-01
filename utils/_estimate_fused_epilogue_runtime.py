
def _estimate_fused_epilogue_runtime(node1, node2, epilogue_runtime) -> float:
    template_write_bytes = node1.get_write_buffer_sizes()
    epilogue_read_bytes = node2.get_read_buffer_sizes()
    extra_bytes = epilogue_read_bytes - template_write_bytes
    # If no extra memory read by epilogue, assume epilogue is free
    # if extra memory is read by epilogue, add to minimum choice
    extra_bytes_ratio = extra_bytes / template_write_bytes

    # Smoothly approaches 1 as extra_bytes_ratio increases
    extra_memory_ratio = extra_bytes_ratio / (1 + extra_bytes_ratio)
    return extra_memory_ratio * epilogue_runtime

