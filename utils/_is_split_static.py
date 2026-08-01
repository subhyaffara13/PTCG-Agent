
def _is_split_static(split_size_or_sizes, _outputs):
    if _outputs is None:
        return False
    if (
        _is_value(split_size_or_sizes)
        and split_size_or_sizes.node().kind() != "onnx::Constant"
    ):
        return False
    return True

