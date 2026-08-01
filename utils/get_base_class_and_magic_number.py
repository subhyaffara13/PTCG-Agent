
def get_base_class_and_magic_number(
    lib_file: BufferedIOBase,
    seek: int | None = None,
) -> tuple[type[ctypes.Structure], int]:
    if seek is None:
        seek = lib_file.tell()
    else:
        lib_file.seek(seek)
    magic_number = ctypes.c_uint32.from_buffer_copy(
        lib_file.read(ctypes.sizeof(ctypes.c_uint32))
    ).value

    # Handle wrong byte order
    if magic_number in [FAT_CIGAM, FAT_CIGAM_64, MH_CIGAM, MH_CIGAM_64]:
        if sys.byteorder == "little":
            BaseClass = ctypes.BigEndianStructure
        else:
            BaseClass = ctypes.LittleEndianStructure

        magic_number = swap32(magic_number)
    else:
        BaseClass = ctypes.Structure

    lib_file.seek(seek)
    return BaseClass, magic_number

