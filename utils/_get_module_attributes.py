
def _get_module_attributes(module):
    annotations = typing.get_type_hints(type(module))
    base_m_annotations = typing.get_type_hints(torch.nn.Module)
    [annotations.pop(k, None) for k in base_m_annotations]
    # Check whether module attributes can be accessed. Some classes
    # define attributes but don't provide access to them in their
    # constructor.
    #
    # For example, torch.nn.Embedding has the `freeze` variable and its
    # type specified in the class but the attribute is not created in the
    # constructor. In other words, there is no `self.freeze = <True | False>`
    # in the constructor.
    #
    # Reference: https://github.com/pytorch/pytorch/blob/92de1d322223fb5584e384971b32c46b93bc2f4b/torch/nn/modules/sparse.py#L120
    attrs = {}
    for k in annotations:
        try:
            attrs[k] = getattr(module, k)
        except AttributeError:
            _C._jit_onnx_log(f"Skipping module attribute '{k}'")
            continue
    return attrs

