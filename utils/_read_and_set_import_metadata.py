
def _read_and_set_import_metadata(data: ReadBuffer, stmt: Import | ImportFrom | ImportAll) -> None:
    read_loc(data, stmt)

    # Metadata flags as a single integer bitfield
    flags = read_int(data)

    # Extract individual flags using bitwise operations
    # Bit 0: is_top_level
    # Bit 1: is_unreachable
    # Bit 2: is_mypy_only
    stmt.is_top_level = (flags & 0x01) != 0
    stmt.is_unreachable = (flags & 0x02) != 0
    stmt.is_mypy_only = (flags & 0x04) != 0

