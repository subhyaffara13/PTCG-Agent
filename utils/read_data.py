
def read_data(struct_class: type[ctypes.Structure], lib_file: BufferedIOBase):
    return struct_class.from_buffer_copy(lib_file.read(ctypes.sizeof(struct_class)))

