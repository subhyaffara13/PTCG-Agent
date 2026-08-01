
def _backend_tag(backend_name, obj):
    if backend_name == "privateuse1":
        backend_name = torch._C._get_privateuse1_backend_name()
    if obj.device.type == backend_name:
        if obj.device.index is None:
            return backend_name
        else:
            return backend_name + ":" + str(obj.device.index)

