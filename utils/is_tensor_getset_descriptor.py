
def is_tensor_getset_descriptor(name: str) -> bool:
    try:
        attr = inspect.getattr_static(torch.Tensor, name)
        return type(attr) is types.GetSetDescriptorType
    except AttributeError:
        return False

