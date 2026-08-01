
def _is_mutable_node(tgt):
    if str(tgt).endswith("_"):
        # e.g. torch.mul_, torch.Tensor.mul_
        return True
    if (
        hasattr(tgt, "__module__")
        and tgt.__module__ == "_operator"
        and tgt.__name__.startswith("i")
    ):
        # e.g. operator.iand, operator.imul
        return True
    return False

