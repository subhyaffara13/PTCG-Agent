
def try_get_name(x):
    if isinstance(x, TensorBox):
        x = x.data
    if isinstance(x, BaseView):
        x = x.unwrap_view()
    if isinstance(x, StorageBox):
        x = x.data
    return x.get_name() if isinstance(x, Buffer) else None

