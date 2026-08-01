
def _extract_tensors(obj):
    r"""
    This function is exclusively called from C++.
    See ``torch/csrc/jit/python/python_ivalue.h``.

    It extracts the tensors contained in the given object, through pickling.
    """
    tensors: list[torch.Tensor] = []
    extractor = _TensorExtractor(io.BytesIO(), protocol=-1, tensors=tensors)
    extractor.dump(obj)
    return tensors

