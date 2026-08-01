
def _item_aten_no_python_dispatcher(*args, **kwargs):
    with torch._dispatch.python.no_python_dispatcher():
        return torch.Tensor.item(*args, **kwargs)

