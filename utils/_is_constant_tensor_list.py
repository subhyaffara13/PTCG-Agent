
def _is_constant_tensor_list(node) -> bool | None:
    if node.kind() != "prim::Constant":
        return False
    output_type = node.output().type()
    if output_type.isSubtypeOf(_C.ListType.ofTensors()):
        return True
    if output_type.isSubtypeOf(_C.ListType(_C.OptionalType.ofTensor())):
        return True

