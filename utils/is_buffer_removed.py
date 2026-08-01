
def is_buffer_removed(name: str) -> bool:
    return any(
        name in x
        for x in (
            V.graph.removed_buffers,
            V.kernel.removed_buffers,
            V.graph.inplaced_to_remove,
            V.kernel.inplaced_to_remove,
        )
    )

