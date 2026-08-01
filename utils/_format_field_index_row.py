
def _format_field_index_row(field_size: int) -> str:
    """Index row aligned under the field, single character per cell."""
    return "".join(str(i % 10) for i in range(field_size))

