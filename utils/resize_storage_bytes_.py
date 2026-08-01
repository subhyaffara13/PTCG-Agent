
def resize_storage_bytes_(variable, new_size):
    variable.realize()
    ir.ResizeStorageBytes(variable, new_size)
    return variable

